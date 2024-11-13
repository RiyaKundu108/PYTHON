PPublic class Opporrunity handlrr{public static void processOpportunities(List<Opportunity> oppList) {
    Set<String> emails = new Set<String>();
    Set<String> phones = new Set<String>();
    Map<Id, Opportunity> oppsToUpdate = new Map<Id, Opportunity>();
    
    // Collect emails and phones from Opportunity records
    for (Opportunity opp : oppList) {
        emails.add(opp.Email__c);
        phones.add(opp.Phone__c);
    }
    
    // Fetch Leads with matching email or phone
    Map<String, Lead> leadsByEmail = new Map<String, Lead>();
    Map<String, Lead> leadsByPhone = new Map<String, Lead>();
    
    List<Lead> matchingLeads = [SELECT Id, Email, Phone, Status FROM Lead 
                                WHERE (Email IN :emails OR Phone IN :phones) 
                                AND Status != 'Converted'];
    
    for (Lead lead : matchingLeads) {
        if (lead.Email != null) leadsByEmail.put(lead.Email, lead);
        if (lead.Phone != null) leadsByPhone.put(lead.Phone, lead);
    }
    
    // Process each Opportunity
    for (Opportunity opp : oppList) {
        Lead matchingLead = leadsByEmail.get(opp.Email__c) != null ? 
                            leadsByEmail.get(opp.Email__c) : 
                            leadsByPhone.get(opp.Phone__c);
        
        if (matchingLead != null) {
            // Convert Lead to Account and Contact if found
            convertLeadToAccountAndContact(matchingLead, opp, oppsToUpdate);
        } else {
            // Create new Account and Contact if no matching Lead found
            createAccountAndContactFromOpportunity(opp, oppsToUpdate);
        }
    }
    
    // Update Opportunities outside of trigger context
    if (!oppsToUpdate.isEmpty()) {
        update oppsToUpdate.values();
    }
}

private static void convertLeadToAccountAndContact(Lead lead, Opportunity opp, Map<Id, Opportunity> oppsToUpdate) {
    Database.LeadConvert lc = new Database.LeadConvert();
    lc.setLeadId(lead.Id);
    lc.setConvertedStatus('Closed - Converted');  
    lc.setDoNotCreateOpportunity(true);
    
    // Create a new Account and set its RecordTypeId
    Account newAccount = new Account();
    newAccount.Name = opp.Customer_Name__c;
    
    if (opp.RecordType.Name == 'Retail') {
        newAccount.RecordTypeId = getRecordTypeId('Account', 'Retail');
    } else if (opp.RecordType.Name == 'Wholesale') {
        newAccount.RecordTypeId = getRecordTypeId('Account', 'Wholesale');
    }
    
    insert newAccount;
    
    lc.setAccountId(newAccount.Id);
    
    Database.LeadConvertResult lcr = Database.convertLead(lc);
    
    // Link Opportunity to the newly created Account and Contact
    if (lcr.isSuccess()) {
        Opportunity updatedOpp = new Opportunity(Id = opp.Id);
        updatedOpp.AccountId = lcr.getAccountId();
        oppsToUpdate.put(updatedOpp.Id, updatedOpp);
    }
}

private static void createAccountAndContactFromOpportunity(Opportunity opp, Map<Id, Opportunity> oppsToUpdate) {
    Account account = new Account();
    account.Name = opp.Customer_Name__c;
    
    if (opp.RecordType.DeveloperName == 'Retail') {
        account.RecordTypeId = getRecordTypeId('Account', 'Retail');
    } else if (opp.RecordType.Name == 'Wholesale') {
        account.RecordTypeId = getRecordTypeId('Account', 'Wholesale');
    }
    
    insert account;
    
    Contact contact = new Contact();
    contact.AccountId = account.Id;
    contact.LastName = opp.Customer_Name__c;
    contact.Email = opp.Email__c;
    contact.Phone = opp.Phone__c;
    insert contact;
    
    Opportunity updatedOpp = new Opportunity(Id = opp.Id);
    updatedOpp.AccountId = account.Id;
    oppsToUpdate.put(updatedOpp.Id, updatedOpp);
}

private static Id getRecordTypeId(String sObjectType, String recordTypeName) {
    return [SELECT Id FROM RecordType 
            WHERE SObjectType = :sObjectType 
            AND Name = :recordTypeName LIMIT 1].Id;
}} in these code when i am creating opportunity of retail type thematching leaa is bring converted but when i am crearing wholesale record typr opportunity it is giving problem please resolvr the issue class OpportunityHelper {
    
    public static void processOpportunities(List<Opportunity> oppList) {
        Set<String> emails = new Set<String>();
        Set<String> phones = new Set<String>();
        Map<Id, Opportunity> oppsToUpdate = new Map<Id, Opportunity>();
        
        // Collect emails and phones from Opportunity records
        for (Opportunity opp : oppList) {
            emails.add(opp.Email__c);
            phones.add(opp.Phone__c);
        }
        
        // Fetch Leads with matching email or phone
        Map<String, Lead> leadsByEmail = new Map<String, Lead>();
        Map<String, Lead> leadsByPhone = new Map<String, Lead>();
        
        List<Lead> matchingLeads = [SELECT Id, Email, Phone, Status FROM Lead 
                                    WHERE (Email IN :emails OR Phone IN :phones) 
                                    AND Status != 'Converted'];
        
        for (Lead lead : matchingLeads) {
            if (lead.Email != null) leadsByEmail.put(lead.Email, lead);
            if (lead.Phone != null) leadsByPhone.put(lead.Phone, lead);
        }
        
        // Process each Opportunity
        for (Opportunity opp : oppList) {
            Lead matchingLead = leadsByEmail.get(opp.Email__c) != null ? 
                                leadsByEmail.get(opp.Email__c) : 
                                leadsByPhone.get(opp.Phone__c);
            
            if (matchingLead != null) {
                // Convert Lead to Account and Contact if found
                convertLeadToAccountAndContact(matchingLead, opp, oppsToUpdate);
            } else {
                // Create new Account and Contact if no matching Lead found
                createAccountAndContactFromOpportunity(opp, oppsToUpdate);
            }
        }
        
        // Update Opportunities outside of trigger context
        if (!oppsToUpdate.isEmpty()) {
            update oppsToUpdate.values();
        }
    }
    
    private static void convertLeadToAccountAndContact(Lead lead, Opportunity opp, Map<Id, Opportunity> oppsToUpdate) {
        Database.LeadConvert lc = new Database.LeadConvert();
        lc.setLeadId(lead.Id);
        lc.setConvertedStatus('Closed - Converted');  
        lc.setDoNotCreateOpportunity(true);
        
        // Create a new Account and set its RecordTypeId
        Account newAccount = new Account();
        newAccount.Name = opp.Customer_Name__c;
        
        if (opp.RecordType.Name == 'Retail') {
            newAccount.RecordTypeId = getRecordTypeId('Account', 'Retail');
        } else if (opp.RecordType.Name == 'Wholesale') {
            newAccount.RecordTypeId = getRecordTypeId('Account', 'Wholesale');
        }
        
        insert newAccount;
        
        lc.setAccountId(newAccount.Id);
        
        Database.LeadConvertResult lcr = Database.convertLead(lc);
        
        // Link Opportunity to the newly created Account and Contact
        if (lcr.isSuccess()) {
            Opportunity updatedOpp = new Opportunity(Id = opp.Id);
            updatedOpp.AccountId = lcr.getAccountId();
            oppsToUpdate.put(updatedOpp.Id, updatedOpp);
        }
    }
    
    private static void createAccountAndContactFromOpportunity(Opportunity opp, Map<Id, Opportunity> oppsToUpdate) {
        Account account = new Account();
        account.Name = opp.Customer_Name__c;
        
        if (opp.RecordType.DeveloperName == 'Retail') {
            account.RecordTypeId = getRecordTypeId('Account', 'Retail');
        } else if (opp.RecordType.Name == 'Wholesale') {
            account.RecordTypeId = getRecordTypeId('Account', 'Wholesale');
        }
        
        insert account;
        
        Contact contact = new Contact();
        contact.AccountId = account.Id;
        contact.LastName = opp.Customer_Name__c;
        contact.Email = opp.Email__c;
        contact.Phone = opp.Phone__c;
        insert contact;
        
        Opportunity updatedOpp = new Opportunity(Id = opp.Id);
        updatedOpp.AccountId = account.Id;
        oppsToUpdate.put(updatedOpp.Id, updatedOpp);
    }
    
    private static Id getRecordTypeId(String sObjectType, String recordTypeName) {
        return [SELECT Id FROM RecordType 
                WHERE SObjectType = :sObjectType 
                AND Name = :recordTypeName LIMIT 1].Id;
    }
}
