import unittest
from inventoryallocator import InventoryAllocator, WareHouse

class TestInventoryAllocator(unittest.TestCase):
  def setUp(self):
    #[ { name: owd, inventory: { apple: 5, orange: 10 } }, { name: dm:, inventory: { banana: 5, orange: 10 } } ]
    #initialize warehouse
    wh1=WareHouse('owd',{ 'apple': 5, 'orange': 10})
    wh2=WareHouse('dm',{ 'banana': 5, 'orange': 10 })
    wh3=WareHouse('wh3',{ 'apple': 5, 'orange': 10, 'banana':10 })
    wh4=WareHouse('wh4',{'apple':1})
    wh5=WareHouse('wh5',{'apple':0})
    wh6=WareHouse('wh6',{'apple':5})
    wh7=WareHouse('wh7',{'apple':5})

    self.wh1=wh1
    self.wh2=wh2
    
    #initialize inventory_allocator
    self.inventory_allocator1=InventoryAllocator({ "apple": 5, "banana": 5, "orange": 5 },[wh1,wh2])
    self.inventory_allocator2=InventoryAllocator({ "apple": 5, "banana": 5, "orange": 5 },[wh1,wh3])
    self.inventory_allocator3=InventoryAllocator({ "green_apple": 5, "banana": 5, "orange": 5 },[wh1,wh3])
    self.inventory_allocator4=InventoryAllocator({'apple':1},[wh4])
    self.inventory_allocator5=InventoryAllocator({'apple':1},[wh5])
    self.inventory_allocator6=InventoryAllocator({'apple':10},[wh6,wh7])
    self.inventory_allocator7=InventoryAllocator({'apple':3, 'orange':11, 'banana':1},[wh1,wh3])
    self.inventory_allocator8=InventoryAllocator({'apple':-1, 'orange':11, 'banana':1},[wh1,wh3])
    self.inventory_allocator9=InventoryAllocator({'apple':100, 'orange':11, 'banana':1},[wh1,wh2,wh3,wh4,wh5,wh6,wh7])
    self.inventory_allocator10=InventoryAllocator({'apple':21, 'orange':11, 'banana':1},[wh1,wh2,wh3,wh4,wh5,wh6,wh7])



  def tearDown(self):
    pass

  def test_constructor(self):
    self.assertEqual(self.inventory_allocator1.order, { "apple": 5, "banana": 5, "orange": 5 })
    self.assertEqual(self.inventory_allocator1.warehouse_list, [self.wh1,self.wh2])

  def test_cheapest_ship(self):
    #normal case
    self.assertEqual(self.inventory_allocator1.cheapest_ship(),
    [{'owd': {'apple': 5, 'orange': 5}}, {'dm': {'banana': 5}}])
    #exist overlap in items among warehouses, want to take 
    #as much as possible from cheapest warehouse
    self.assertEqual(self.inventory_allocator2.cheapest_ship(),
    [{'owd': {'apple': 5, 'orange': 5}}, {'wh3': {'banana': 5}}])
    #some item doesn't exist in all warehouses
    self.assertEqual(self.inventory_allocator3.cheapest_ship(),
    [])
    #Happy Case, exact inventory match!*
    self.assertEqual(self.inventory_allocator4.cheapest_ship(),
    [{ 'wh4': { 'apple': 1 } }])
    #Not enough inventory -> no allocations!
    self.assertEqual(self.inventory_allocator5.cheapest_ship(),
    [])
    #Should split an item across warehouses 
    #if that is the only way to completely ship an item:
    self.assertEqual(self.inventory_allocator6.cheapest_ship(),
    [{ 'wh6': { 'apple': 5 }}, { 'wh7': { 'apple': 5 } }])
    #some need to be splitted across warehouse while other can be handled by one
    self.assertEqual(self.inventory_allocator7.cheapest_ship(),
    [{'owd': {'apple': 3, 'orange': 10}}, {'wh3': {'orange': 1, 'banana': 1}}])
    #edge case, negative number for order
    self.assertEqual(self.inventory_allocator8.cheapest_ship(),[])
    #multiple warehouse but still not enough->no alloctions!
    self.assertEqual(self.inventory_allocator9.cheapest_ship(),[])
    #just enought one item, other item also enough for multiple warehouses
    self.assertEqual(self.inventory_allocator10.cheapest_ship(),
    [{'owd': {'apple': 5, 'orange': 10}},
    {'dm': {'banana': 1, 'orange': 1}},
    {'wh3': {'apple': 5}},
    {'wh4': {'apple': 1}},
    {'wh6': {'apple': 5}},
    {'wh7': {'apple': 5}}])



    #print(self.inventory_allocator2.cheapest_ship())
    
    
if __name__=='__main__':
  unittest.main()