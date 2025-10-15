For selecting invoice status in commissions:

#. Edit or create a new record to select the invoice status for settling the commissions.

   * **Invoice Based**: Commissions are settled when the invoice is issued.
   * **Payment Based**: Commissions are settled when the invoice is paid or refunded.
     Note that when refunding an invoice, the corresponding reversed commission will
     be settled as well, resulting in a 0 net commission between both operations.

#. For payment-based commissions, you can choose how settlements are grouped. 
By default, they’re grouped by 'Invoice Date', but you can also group them 
by 'Payment Date'. 
For example, if you select 'Payment Date', all commissions
related to payments made on the same period will be grouped together in a single settlement.
