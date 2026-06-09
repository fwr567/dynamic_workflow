# Copyright (c) 2024, Your Company
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.utils import today
from datetime import datetime


class DelegationEngine:
    """
    Approval Delegation Engine
    
    Manages approval delegation to other users
    """

    @staticmethod
    def sync_delegations():
        """Sync delegation status (check expiry)"""
        
        try:
            current_date = today()
            
            # Find expired delegations
            expired_delegations = frappe.get_all(
                'Approval Delegation',
                filters=[
                    ['to_date', '<', current_date],
                    ['status', '=', 'Active']
                ]
            )
            
            for delegation in expired_delegations:
                delegation_doc = frappe.get_doc('Approval Delegation', delegation['name'])
                delegation_doc.status = 'Expired'
                delegation_doc.save()
        
        except Exception as e:
            frappe.log_error(f"Error syncing delegations: {str(e)}")

    @staticmethod
    def get_delegatee(approver, doc_type=None):
        """Get delegatee if user has delegation"""
        
        try:
            current_date = today()
            
            delegations = frappe.get_all(
                'Approval Delegation',
                filters=[
                    ['delegator', '=', approver],
                    ['from_date', '<=', current_date],
                    ['to_date', '>=', current_date],
                    ['is_active', '=', 1],
                    ['status', '=', 'Active']
                ]
            )
            
            for delegation in delegations:
                delegation_doc = frappe.get_doc('Approval Delegation', delegation['name'])
                
                # Check document type restriction
                if delegation_doc.document_types:
                    doc_types = [dt.strip() for dt in delegation_doc.document_types.split(',')]
                    if doc_type not in doc_types:
                        continue
                
                return delegation_doc.delegatee
            
            return approver
        
        except Exception as e:
            frappe.log_error(f"Error getting delegatee: {str(e)}")
            return approver
