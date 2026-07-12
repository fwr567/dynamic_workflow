import frappe
from frappe import _

import requests
import json


class WeChatIntegration:
    """Handles WeChat Work (企业微信) notification integration."""

    @staticmethod
    def send_approval_notification(approver_user, document_type, document_name):
        """
        Send a WeChat notification to an approver about a pending approval.

        Args:
            approver_user: User email ID of the approver.
            document_type: DocType of the document.
            document_name: Name of the document.
        """
        config = WeChatIntegration._get_config()
        if not config or not config.get("enable_wechat"):
            return

        access_token = WeChatIntegration._get_access_token(config)
        if not access_token:
            frappe.log_error(
                title="WeChat Integration Error",
                message="Failed to obtain access token.",
            )
            return

        doc_link = frappe.utils.get_url_to_form(document_type, document_name)
        message = (
            f"您有一条待审批单据:\n"
            f"单据类型: {document_type}\n"
            f"单据编号: {document_name}\n"
            f"查看详情: {doc_link}"
        )

        wechat_user_id = WeChatIntegration._get_wechat_user_id(approver_user)
        if not wechat_user_id:
            frappe.log_error(
                title="WeChat Integration Warning",
                message=f"No WeChat user ID found for {approver_user}",
            )
            return

        WeChatIntegration._post_message(
            access_token, config.get("agent_id"), wechat_user_id, message
        )

    @staticmethod
    def _get_config():
        """
        Get WeChat integration configuration from Dynamic Workflow Config
        or site_config.json.

        Returns:
            dict: Configuration dict or None.
        """
        try:
            site_config = frappe.conf
            return {
                "enable_wechat": site_config.get("dw_wechat_enabled", False),
                "corp_id": site_config.get("dw_wechat_corp_id", ""),
                "corp_secret": site_config.get("dw_wechat_corp_secret", ""),
                "agent_id": site_config.get("dw_wechat_agent_id", ""),
            }
        except Exception as e:
            frappe.log_error(
                title="WeChat Integration - Config Error",
                message=str(e),
            )
            return None

    @staticmethod
    def _get_access_token(config):
        """
        Obtain a WeChat Work access token using corp_id and corp_secret.

        Args:
            config: Configuration dict from _get_config().

        Returns:
            str: Access token or None.
        """
        if not config.get("corp_id") or not config.get("corp_secret"):
            return None

        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": config["corp_id"],
            "corpsecret": config["corp_secret"],
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            if data.get("errcode") == 0:
                return data.get("access_token")
            else:
                frappe.log_error(
                    title="WeChat Integration - Token Error",
                    message=f"errcode: {data.get('errcode')}, errmsg: {data.get('errmsg')}",
                )
                return None
        except Exception as e:
            frappe.log_error(
                title="WeChat Integration - Token Request Failed",
                message=str(e),
            )
            return None

    @staticmethod
    def _post_message(access_token, agent_id, user_id, content):
        """
        Send a text message via WeChat Work API.

        Args:
            access_token: WeChat access token.
            agent_id: WeChat agent ID.
            user_id: WeChat user ID.
            content: Message content string.
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
        params = {"access_token": access_token}
        payload = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": agent_id,
            "text": {"content": content},
        }

        try:
            response = requests.post(
                url, params=params, json=payload, timeout=10
            )
            data = response.json()
            if data.get("errcode") != 0:
                frappe.log_error(
                    title="WeChat Integration - Send Message Error",
                    message=f"errcode: {data.get('errcode')}, errmsg: {data.get('errmsg')}",
                )
        except Exception as e:
            frappe.log_error(
                title="WeChat Integration - Send Failed",
                message=str(e),
            )

    @staticmethod
    def _get_wechat_user_id(frappe_user):
        """
        Map a Frappe user to a WeChat Work user ID.

        By default, uses the Frappe user email as the WeChat user ID.
        Override this method or add a custom field on User for mapping.

        Args:
            frappe_user: Frappe user email ID.

        Returns:
            str: WeChat user ID or None.
        """
        wechat_id = frappe.db.get_value("User", frappe_user, "wechat_user_id")
        if wechat_id:
            return wechat_id
        return frappe_user
