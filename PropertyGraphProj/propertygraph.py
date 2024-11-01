"""
File: propertygraph.py
Description: An implementation of a PropertyGraph consisting of
Node and Relationship objects.  Nodes and Relationships carry
properties.  Property graphs are used to represent connected knowledge.

rename
"""


class Node:

    def __init__(self, name, category, props=None):
        """ Class constructor """
        self.name = str(name) #String name of node
        self.category = str(category) #Sting category of node which is only Person or Book
        self.props = props if props is not None else {} #Dictionary of properties which is 

    def __getitem__(self, key):
        """ Fetch a property from the node using [] return None if property doesn't exist 

        Parameters:
        self (Node)
        key (str): String of the property key that we would like to get its property values

        Returns:
        self.props[key] (str): this will give the values of key
         """
        return self.props[key]

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] 
        Parameters:
        self (Node)
        key (str): String of the property key
        value (str): Value we would like to add to key in props dictionary

        (Setter Function)
        self.props[key] = value : this will add property keys and its values for a node
        """
        self.props[key] = value

    def __eq__(self, other):
        """ Two nodes are equal if they have the same name and category irrespective of their properties 
        Parameters:
        self (Node)
        other (Node): Node object to check equality against
        
        Returns:
        (boolean) weather they are equal based on catagory and name
        """
        if isinstance(other, Node):
            return (self.name,self.category) == (other.name,other.category)
        return False

    def __hash__(self):
        """ By making Nodes hashable we can now store them as keys in a dictionary! based on name and catagory
        Parameters:
        self (Node)
        
        Returns:
        hash (int) of name and catagory of Node object using built in hash function
        """
        return hash((self.name , self.category ))

    def __repr__(self):
        """ Output the node as a string in the following format:
        name:category<tab>properties.
        Note: __repr__ is more versatile than __str__ 
        
        Retruns
        (str) in the specified form above
        """
        return f"{self.name}:{self.category}\t{self.props}"


class Relationship:

    def __init__(self, category, props=None): #Relationship Object takes a catagory and properties in a dictionary
            self.category = str(category) #String of catagory either, Knows or Bought
            self.props = props if props is not None else {} #Dictionary for additional properties that may be needed

    def __getitem__(self, key):
        """ Fetch a property from the node using [] return None if property doesn't exist 
        Parameters:
        self (Relationship)
        Key (str): String of key of the property you want to get
        
        Returns:
        self.props[key](str) which is the value of the specified property key
        """
        if isinstance(key, self.props.keys()):
            return self.props[key]
        return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] 
        Parameters:
        self (Relationship)
        Key (str): String of key of the property you want to get
        value (str): Sring of the value we want to associate with property in our props dictionary
        
        (Setter Function):
        Sets self.props[key] which is the value of the specified property key
        """
        self.props[key] = value

    def __repr__(self):
        """ Output the relationship as a string in the following format:
        :category<space>properties.
        Note: __repr__ is more versatile than __str__ 
        
        Retruns
        (str) in the specified form above
        """
        return f":{self.category} {self.props}"


class PropertyGraph:
# graph = {node: [(targ,rel),(targ,rel)], 
#          node: [(targ,rel),(targ,rel)]}

    def __init__(self):
        """ Construct an empty property graph """
        self.graph = {} #graph is a dictionary

    def add_node(self, node):
        """ Add a node to the property graph 
        Parameters:
        self (PropertyGraph)
        node (Node): Node object we would like to add to our graph dictionary
        
        (Setter Function):
        Sets graph[node] = [] which is a node key withought a value
        """
        self.graph[node] = []

    def add_relationship(self, src, targ, rel):
        """ Connect src and targ nodes via the specified directed relationship.
        If either src or targ nodes are not in the graph, add them.
        Note that there can be many relationships between two nodes! 
        
        Parameters:
        self (PropertyGraph)
        src (Node): Source node, key node
        targ (Node): target node, tuple node, that we wanna set rel with
        rel (Relationship): relationship between src and trg
        
        Setter Function:
        Sets graph[src].append((targ,rel)) which will add the tupple trg rel to key node in our property graph if it exists or else will add a new key node
        """
        self.graph[src].append((targ,rel))


    def get_nodes(self, name=None, category=None, key=None, value=None):
        """ Return the SET of nodes matching all the specified criteria.
        If the criterion is None it means that the particular criterion is ignored. 
        
        Parameters:
        self (PropertyGraph)
        name (str): Node object we would like to add to our graph dictionary
        category (str): catagory of the Node we are looking for
        key (str): key of any property the node might have
        value (str): values of any property the node might have
        
        Returns:
        Result (tuple): returns a tupe of node objects of the criteria we are looking for
        """
        result = set()

        for node in self.graph:
            matches = True

            if name is not None and getattr(node, 'name', None) != name:
                matches = False
            if category is not None and getattr(node, 'category', None) != category:
                matches = False
            if key is not None and node.props.get(key) != value:
                matches = False

        if matches:
            result.add(node)

        return result

    def adjacent(self, node, node_category=None, rel_category=None):
        """ Return a set of all nodes that are adjacent to node.
        If specified include only adjacent nodes with the specified node_category.
        If specified include only adjacent nodes connected via relationships with
        the specified rel_category 
        
        Parameters:
        self (PropertyGraph)
        node (Node): Node object for source
        node_category (str): catagory of the node we want to find ajancent with
        rel_catagory (str): catagory of the Relationship we want to find ajancent with
        
        Returns:
        Result (tuple): returns a tupe of node objects of the criteria that are adjacent to node
        """
        result = set()
        if node in self.graph:
            for target, rel in self.graph[node]:
                if (node_category is None or target.category == node_category) and (rel_category is None or rel.category == rel_category):
                    result.add(target)
        return result
            
#
    def subgraph(self, nodes):
        """ Return the subgraph as a PropertyGraph consisting of the specified
        set of nodes and all interconnecting relationships

        Parameters:
        self (PropertyGraph)
        node (tuple): takes a tuple of sub nodes made with methods above and makes a subgraph of their relationships
        
        Returns:
        sub (PropertyGraph): returns a PropertyGraph of nodes

        """
        sub = PropertyGraph()
        for node in nodes:
            if node in self.graph:
                sub.add_node(node)
                for targ, rel in self.graph[node]:
                    if targ in nodes:
                        sub.add_relationship(node, targ, rel)


                sub.add_node(node)
        return sub

    def __repr__(self):
        """ A string representation of the property graph
        Properties are not displaced.

        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        .
        .
        etc.
        """
        result = []
        for node, Relationship in self.graph.items():
            result.append(f"{node}")
            for targ, rel in Relationship:
                result.append(f"     {rel} {targ} ")
        return ("\n".join(result))

