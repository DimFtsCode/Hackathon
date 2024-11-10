import networkx as nx

def create_graph_with_intermediate():
    G = nx.DiGraph()
    source = 's'
    sink = 't'

    # Σκυλιά και πιάτα (μόνο 2 πιάτα για να προκαλέσουμε περιορισμό)
    dogs = ['dog1', 'dog2']
    plates = ['plate1', 'plate2']

    # Προσθήκη πηγής και καταβόθρας
    G.add_node(source)
    G.add_node(sink)

    # Δημιουργία των ενδιάμεσων κόμβων και προσθήκη των ενδιάμεσων ακμών
    for dog in dogs:
        dog_in = f"{dog}_in"
        dog_out = f"{dog}_out"
        G.add_node(dog_in)
        G.add_node(dog_out)
        
        # Σύνδεση της πηγής με το dog_in με χωρητικότητα 2
        G.add_edge(source, dog_in, capacity=2)
        
        # Σύνδεση του dog_in με το dog_out με χωρητικότητα 2
        G.add_edge(dog_in, dog_out, capacity=2)

    # Προσθήκη πιάτων και σύνδεση με καταβόθρα
    for plate in plates:
        G.add_node(plate)
        G.add_edge(plate, sink, capacity=1)

    # Σύνδεση των dog_out με πιάτα (κάθε σκυλί μπορεί να φάει από τα ίδια πιάτα)
    G.add_edge('dog1_out', 'plate1', capacity=1)
    G.add_edge('dog1_out', 'plate2', capacity=1)
    
    G.add_edge('dog2_out', 'plate1', capacity=1)
    G.add_edge('dog2_out', 'plate2', capacity=1)

    return G

def create_graph_without_intermediate():
    G = nx.DiGraph()
    source = 's'
    sink = 't'

    # Σκυλιά και πιάτα (μόνο 2 πιάτα για να προκαλέσουμε περιορισμό)
    dogs = ['dog1', 'dog2']
    plates = ['plate1', 'plate2']

    # Προσθήκη πηγής και καταβόθρας
    G.add_node(source)
    G.add_node(sink)

    # Προσθήκη σκυλιών και σύνδεση με πηγή
    for dog in dogs:
        G.add_node(dog)
        G.add_edge(source, dog, capacity=2)

    # Προσθήκη πιάτων και σύνδεση με καταβόθρα
    for plate in plates:
        G.add_node(plate)
        G.add_edge(plate, sink, capacity=1)

    # Σύνδεση των σκυλιών με τα πιάτα
    G.add_edge('dog1', 'plate1', capacity=1)
    G.add_edge('dog1', 'plate2', capacity=1)
    
    G.add_edge('dog2', 'plate1', capacity=1)
    G.add_edge('dog2', 'plate2', capacity=1)

    return G

# Δημιουργία γραφήματος με ενδιάμεσες ακμές
G_with_intermediate = create_graph_with_intermediate()

# Δημιουργία γραφήματος χωρίς ενδιάμεσες ακμές
G_without_intermediate = create_graph_without_intermediate()

# Υπολογισμός μέγιστης ροής για τον γράφο με ενδιάμεσες ακμές
flow_value_with, flow_dict_with = nx.maximum_flow(G_with_intermediate, 's', 't')

# Υπολογισμός μέγιστης ροής για τον γράφο χωρίς ενδιάμεσες ακμές
flow_value_without, flow_dict_without = nx.maximum_flow(G_without_intermediate, 's', 't')

# Εκτύπωση αποτελεσμάτων για γράφο με ενδιάμεσες ακμές
print("Με ενδιάμεσους κόμβους:")
print(f"Μέγιστη ροή: {flow_value_with}")
happy_dogs_with = 0
for dog in ['dog1', 'dog2']:
    dog_out = f"{dog}_out"
    outflow = sum(flow_dict_with[dog_out].values())
    if outflow == 2:
        happy_dogs_with += 1
        print(f"{dog} έλαβε δύο πιάτα και είναι χαρούμενο.")
    else:
        print(f"{dog} δεν έλαβε δύο πιάτα και δεν είναι χαρούμενο.")
print(f"Συνολικός αριθμός χαρούμενων σκυλιών: {happy_dogs_with}")

# Εκτύπωση αποτελεσμάτων για γράφο χωρίς ενδιάμεσες ακμές
print("\nΧωρίς ενδιάμεσους κόμβους:")
print(f"Μέγιστη ροή: {flow_value_without}")
happy_dogs_without = 0
for dog in ['dog1', 'dog2']:
    outflow = sum(flow_dict_without[dog].values())
    if outflow == 2:
        happy_dogs_without += 1
        print(f"{dog} έλαβε δύο πιάτα και είναι χαρούμενο.")
    else:
        print(f"{dog} δεν έλαβε δύο πιάτα και δεν είναι χαρούμενο.")
print(f"Συνολικός αριθμός χαρούμενων σκυλιών: {happy_dogs_without}")
