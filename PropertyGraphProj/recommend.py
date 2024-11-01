"""
Your book recommendation engine demonstrating the utility of your
PropertyGraph class. Remember to include the required output in the header of your
program. The expected output is the original property graph, the subgraph containing
Spencer and the books to be recommended, and finally the new property graph with
Spencer linked to the recommended books.

"""
from propertygraph import Node
from propertygraph import Relationship
from propertygraph import PropertyGraph





#initialize nodes
#emily, spencer, brendan, trevor, paxtyn
Emily = Node("Emily","Person")
Spencer = Node("Spencer","Person")
Brendan = Node("Brendan","Person")
Trevor = Node("Trevor","Person")
Paxtyn = Node("Paxtyn","Person")

#Cosmos, Database Design, The Life of Cronkite, DNA & You, Books have price prop
Cosmos = Node("Cosmos","Book",{"Price":"$17.00"})
DataBaseDesign = Node("DataBase Design","Book",{"Price":"$195.00"})
TheLifeofCronkite = Node("The Life of Cronkite","Book",{"Price":"$29.95"})
DNAYou = Node("DNA & You","Book",{"Price":"$11.50"})
Principle = Node("Principles","Book",{"Price":"$39.99"})

#initialize relation
Bought = Relationship("Bought")
Knows = Relationship("Knows")

#Make graph

#origional graph
PropGraph = PropertyGraph()
PropGraph.add_node(Emily)
PropGraph.add_node(Spencer)
PropGraph.add_node(Brendan)
PropGraph.add_node(Trevor)
PropGraph.add_node(Paxtyn)

#Adds our relationships
PropGraph.add_relationship(Emily,DataBaseDesign,Bought)
PropGraph.add_relationship(Emily,Spencer,Knows)
PropGraph.add_relationship(Spencer,Emily,Knows)
PropGraph.add_relationship(Spencer,Cosmos,Bought)
PropGraph.add_relationship(Spencer,DataBaseDesign,Bought)
PropGraph.add_relationship(Spencer,Brendan,Knows)
PropGraph.add_relationship(Spencer,Cosmos,Bought)
PropGraph.add_relationship(Brendan,DataBaseDesign,Bought)
PropGraph.add_relationship(Brendan,DNAYou,Bought)
PropGraph.add_relationship(Trevor,Cosmos,Bought)
PropGraph.add_relationship(Trevor,DataBaseDesign,Bought)
PropGraph.add_relationship(Paxtyn,DataBaseDesign,Bought)
PropGraph.add_relationship(Paxtyn,TheLifeofCronkite,Bought)
PropGraph.add_relationship(Brendan,Principle,Bought)


print(PropGraph) #print our origional graph from assignment page

def recommend_books(graph, person):
    """ 
    Return a subgraph of graph of our recomendations for person. Must be a book that the person does not own but is owned by people they know

    Parameters:
    graph (PropertyGraph)
    person (Node): Node in graph that we want to make recomendations for 
        
    Returns:
    sub (PropertyGraph): returns a PropertyGraph of nodes

    """
    # Find all books bought by people the person knows
    friends = graph.adjacent(person, node_category='Person', rel_category='Knows')
    books_bought_by_friends = set()
    for friend in friends:
        books = graph.adjacent(friend, node_category='Book', rel_category='Bought')
        books_bought_by_friends.update(books)

    # Find all books bought by the person
    books_bought_by_person = graph.adjacent(person, node_category='Book', rel_category='Bought')

    # Exclude books already bought by the person
    recommended_books = books_bought_by_friends - books_bought_by_person

    # Create a subgraph with the person and recommended books
    sub = graph.subgraph({person}.union(recommended_books))

    # Add Recommend relationships
    for book in recommended_books:
        sub.add_relationship(person, book, Relationship('Recommend'))

    return sub

recommendation_graph = recommend_books(PropGraph, Spencer)
print(recommendation_graph)






