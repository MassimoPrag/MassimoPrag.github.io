"""
Your unit tests, one for each method. It is up to you to define
fixtures that generate a simple property graph, and that can be used to validate the
various methods. Your unit test assertions should be comprehensive and cover all edge
cases.

look up unit tests
put this is sperate folder

pytest, fixtures
make methods that return your class object, way to initialize object


difine objects
from property_graph import ----
import pytest
"""
import pytest
from propertygraph import Node
from propertygraph import Relationship
from propertygraph import PropertyGraph

#Node class testing 

def test_init(): #initialize node object, assert every param/attribute
    node = Node("EMY", "Person")
    assert node.name == "EMY", "Should be name passed as first param and of type string"
    assert node.category == "Person" or "Book", "Catagory of nodes can only be person or book and must be string value"
    assert node.props == {}, "must be type dict in this case an empty dict because no dict param is passed"

def test_getitem():#Test to see if we can get a specific properties from the node
    testprops = {"key1":"Val1","key2":"val2"}
    node = Node("EMY", "Person", testprops)
    assert node.props["key1"] == "Val1"

def test_setitem():#test set property item method for nodes
    testprops = {"key1":"Val1","key1":"val2"}
    node = Node("EMY", "Person", testprops)
    node["key3"] = "value3"
    assert node.props["key3"] == "value3" , ""

def test_eq():#tests equality for nodes
    node1 = Node("Jack","Person")
    node2 = Node("Jack","Person")
    assert node1 == node2, "Nodes with the same Name and Catagory will have the same hash and deemed equivilant"

def test_hash():
    node = Node("EMY", "Person")
    node2 = Node("Jack","Person")
    assert isinstance(hash(node), int) # makes sure that the hash of a node gives an interger
    assert hash(node) != hash(node2) #asserts two hashes are not equal

def test_repr(): #tests for required print format
    testprops = {'key1':'Val1','key2':'val2'}
    node = Node("EMY", "Person", testprops) 
    assert repr(node) == "EMY:Person\t{'key1': 'Val1', 'key2': 'val2'}"


#Relationship class testing

@pytest.fixture
def rel(): #Fixture
    return Relationship("Bought", {"Key1":"Val1"})

def test_rel_init(rel): 
    assert rel.category == "Bought" #tests that our first param is catagory
    assert rel.props == {"Key1":"Val1"} #tests that our second param is properties

def test_rel_getitem(rel): #tests to see if we can get properties
    assert rel.props["Key1"] == "Val1" ,"Property not found"

def test_rel_setitem(rel): #tests to see if we cant set properties
    rel["Key2"] = "Val2"
    assert rel.props["Key2"] == "Val2"

def test_rel_repr(rel):  #tests for required print format
    assert repr(rel) == ":Bought {'Key1': 'Val1'}"



#Graph class testing

def test_gr_init():
    graph = PropertyGraph()

    assert graph.graph == {} #assert that our object is of type dictionary

def test_gr_add_node(): #tests adding an individual node to our graph
    node = Node("EMY", "Person")
    graph = PropertyGraph()
    graph.add_node(node)
    assert node in graph.graph #is node in the dictionary of graph

def test_gr_add_relationship(): # tests that our relationships are in the graph and match with key nodes
    src = Node("EMY", "Person")
    rel = Relationship("Bought")
    targ = Node("Principles","Book")
    graph = PropertyGraph()
    graph.add_node(src)
    graph.add_relationship(src,targ,rel)
    assert (targ,rel) in graph.graph[src]

def test_gr_get_nodes():
    graph = PropertyGraph()
    
    node1 = Node('A', 'Category1', {'key1': 'value1'})
    node2 = Node('B', 'Category2', {'key2': 'value2'})
    node3 = Node('C', 'Category1', {'key3': 'value3'})
    
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    
    # Test filtering by name
    result = graph.get_nodes(name='A')
    assert result == {node1}
    
    # Test filtering by category
    result = graph.get_nodes(category='Category1')
    assert result == {node1, node3}
    
    # Test filtering by property key and value
    result = graph.get_nodes(key='key1', value='value1')
    assert result == {node1}
    
    # Test with no criteria (should return all nodes)
    result = graph.get_nodes()
    assert result == {node1, node2, node3}

def test_gr_adjacent(): #tests if nodes are adjacent
    graph = PropertyGraph()
    
    node1 = Node('A', 'Person')
    node2 = Node('B', 'Book')
    node3 = Node('C', 'Person')
    
    rel1 = Relationship('Knoows')
    rel2 = Relationship('Bought')
    
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    
    graph.add_relationship(node1, node2, rel2)
    graph.add_relationship(node1, node3, rel1)
    
    result1 = graph.adjacent(node1)
    assert result1 == {node2, node3}
    
    result2 = graph.adjacent(node1, node_category='Book')
    assert result2 == {node2}
    
    result3 = graph.adjacent(node1, rel_category='Knows')
    assert result3 == {node3}

def test_gr_subgraph():
    graph = PropertyGraph()
    
    node1 = Node('A', 'Person')
    node2 = Node('B', 'Book')
    node3 = Node('C', 'Person')
    node4 = Node('D', 'Book')
    
    rel1 = Relationship('Knows')
    rel2 = Relationship('Bought')
    
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    graph.add_node(node4)
    
    graph.add_relationship(node1, node2, rel2)
    graph.add_relationship(node1, node3, rel1)
    graph.add_relationship(node2, node4, rel1)
    
    sub = graph.subgraph({node1, node2, node4})
    
    assert (node2, rel2) in sub.graph[node1]
    assert (node4, rel1) in sub.graph[node2]
    assert node3 not in sub.graph

#repr test





#text header












