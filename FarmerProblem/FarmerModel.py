from pyomo.environ import *

#
# Farmer Model
#

def FarmerModel():
    
    infinity = float('inf')
    
    model = AbstractModel()
    
    # Vegetables
    model.V = Set()
    # Resources
    model.R = Set()
    
    # Selling price for each vegetable
    model.c    = Param(model.V, within=PositiveReals)
    # Maximum available quantity of each vegetable
    model.avail = Param(model.V, within=NonNegativeReals)
    #  Maximum available quantity of each resource
    model.max_q = Param(model.R, within=NonNegativeReals)
    # Needed quantity of resource j for vegetable i
    model.need = Param(model.R, model.V, within=NonNegativeReals)
    
    
    # Number of seeds/tuber used for each vegetable
    # bounds for each variable are obtained using domain_rule function
    def domain_rule(model, i):
        return (0.0, model.avail[i])
    model.x = Var(model.V, bounds=domain_rule)

    
    
    # Maximize gain
    def cost_rule(model):
        return sum(model.c[i]*model.x[i] for i in model.V)
    model.cost = Objective(rule=cost_rule, sense=maximize)

    # Limitation on available resources
    def resourceUtil_rule(model, j):
        return sum(model.need[j,i]*model.x[i] for i in model.V) <= model.max_q[j]
    model.resourceUtil = Constraint(model.R, rule=resourceUtil_rule)

    
    return model
