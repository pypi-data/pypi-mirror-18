'''
Object to represent and facilitate Billing operations. All get, add, modify, and delete methods
of API session will return objects defined here instead of JSON. 
'''

class BillPlan(object):
    '''
    BillPlan object. 
    
    :param name: name of bill plan (IE: 'somecompany-billing')
    :type name: str
    :param description: description for bill plan (IE: 'somecompany BS')
    :type description: str
    :param cost_unit: currency (IE: 'USD')
    :type cost_unit: int
    :param period_type: (IE:'monthly')
    :type period_type: str
    :param gen_date: generate date for billing (IE: '1' is first day of month)
    :type gen_date: int
    :param time_zone: Time Zone(IE: 'US/eastern')
    :type time_zone: str
    :param base_speed: speed in bits per second (IE: '50000')
    :type base_speed: int
    :param base_cost: Base cost of alloted bandwith(IE: '500')
    :type base_cost: int
    :param add_speed: Additional speed in bits per second (IE: '1')
    :type add_speed: int
    :param add_cost: Additional cost for every unit of additional speed overage in USD (IE: '600')
    :type add_cost: int
    :param type: billing type, either speed or volumetric (IE: 'speed' or 'volume')
    :type type: str
    :param percent: 95t percentile calculation. 40 for merge, 41 for seperate (IE: '40')
    :type percent: int
    :param intf_id: interface ID bill plan will apply to, if applicable
    :type intf_id: str
    :param ipg_id: comma seperated, IPGroup IDs bill plan will apply to (IE: '2500033,2500027,2500034,2500025')
    :type ipg_id: str
    :param buss_id: ???
    :type buss_id: str
    :param email_id: Email address for bill (IE: 'someonewhocares@somecompany.com')
    :type str:
    :param email_sub: Subject of email (IE: 'billing report for blah blah')
    :type str:

    More info:
    https://www.manageengine.com/products/netflow/help/admin-operations/billing.html
    '''

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.cost_unit = kwargs.get('cost_unit', 'USD')
        self.period_type = kwargs.get('period_type', 'monthly')
        self.gen_date = kwargs.get('gen_date', '1')
        self.time_zone = kwargs.get('time_zone', 'US/eastern')
        self.base_speed = kwargs.get('base_speed')
        self.base_cost = kwargs.get('base_cost')
        self.add_speed = kwargs.get('add_speed')
        self.add_cost = kwargs.get('add_cost')
        self.type = kwargs.get('type', 'speed')
        self.percent = kwargs.get('percent', 40)
        self.buss_id = kwargs.get('buss_id', '')
        self.email_id = kwargs.get('email_id')
        self.email_sub = kwargs.get('email_sub')

        #Interface IDs bill plan applies to
        self.intf_id = kwargs.get('intf_id', '')
        
        #IP Group IDs bill plan applies to
        self.ipg_id = kwargs.get('ipg_id', '')

        #Plan ID, NOT provided at creation!
        self.plan_id = kwargs.get('plan_id', '')

    def __repr__(self):
        return '<BillPlan - Name:{0} Type:{1}'.format(
            self.name,
            self.type
        )

