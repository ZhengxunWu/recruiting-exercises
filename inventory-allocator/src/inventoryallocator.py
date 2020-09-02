class InventoryAllocator:
  def __init__(self, order, warehouse_list):
    
    """a map of items that are being ordered and how many of them are ordered"""
    self.order=order
    """ 
    a list of object with warehouse name and inventory amounts 
    (inventory distribution) for these items
    """
    self.warehouse_list=warehouse_list
    """total amout of item being ordered in this order"""
    self.total_order_amount=0
    for amount in order.values():
      self.total_order_amount+=amount

  def cheapest_ship(self):
    inventory_distribution_res=[]
    #deep copy since need to change value in this function without changing 
    #object's original value
    order=self.order.copy()
    warehouse_list=self.warehouse_list
    total_order_amount=self.total_order_amount
    for warehouse in warehouse_list:
      """
      Let number of warehouses be W, len of longest inventory list for warehouse
      I, len of order R, time complexity O(W* min(I, R))
      """
      traverse_warehouse=len(warehouse.inventory)<len(order)
      cur_warehouse_allocation={}
  
      if traverse_warehouse:
        #len of warehouse inventory is smaller, start traverse warehouse inventory
        for inventory_name, inventory_amount in warehouse.inventory.items():
          #inventory is required in order
          if inventory_name in order:
            amount_assigned=min(inventory_amount, order[inventory_name])
            #handle corner case and amount_assigned cannot be 0
            if amount_assigned<=0: continue
            order[inventory_name]-=amount_assigned
            total_order_amount-=amount_assigned
            cur_warehouse_allocation[inventory_name]=amount_assigned

        if bool(cur_warehouse_allocation):
          #some assignment happend for current warehouse
          appended_dict={}
          appended_dict[warehouse.name]=cur_warehouse_allocation
          inventory_distribution_res.append(appended_dict)
          if total_order_amount==0:
              #all order is assigned, early stop
              return inventory_distribution_res

      #len of warehouse inventory is larger, start traverse order
      else:
        """Note: this part is duplicated code, can be parametrized with above 
        to reduce length of code, here just for readability, not compressed"""
        for order_name, order_amount in order.items():
          if order_amount!=0 and order_name in warehouse.inventory:
            amount_assigned=min(warehouse.inventory[order_name], order_amount)
            #handle corner case and amount_assigned cannot be 0
            if amount_assigned<=0: continue
            order[order_name]-=amount_assigned
            total_order_amount-=amount_assigned
            cur_warehouse_allocation[order_name]=amount_assigned
        
        if bool(cur_warehouse_allocation):
          #some assignment happend for current warehouse
          appended_dict={}
          appended_dict[warehouse.name]=cur_warehouse_allocation
          inventory_distribution_res.append(appended_dict)

          if total_order_amount==0:
              #all order is assigned, early stop
              return inventory_distribution_res
    #after traverse all warehouse, order is still not completely assigned
    return []
            


      
    
class WareHouse:
  def __init__(self,name, inventory):
    self.name=name
    self.inventory=inventory
    


