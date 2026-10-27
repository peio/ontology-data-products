# Ontology Development 101: A Guide to Creating Your First Ontology

# Ontology Development Workflow

## Step 1: Determine Domain and Scope

**Purpose**: Establish the foundation and boundaries of your ontology project.

### Key Questions to Answer:
- **What is the domain that the ontology will cover?**
  - What specific area of knowledge are you modeling?
  - What are the main concepts and relationships in this domain?

- **For what are you going to use the ontology?**
  - What applications will consume this ontology?
  - What problems will it solve?
  - What decisions will it support?

- **What types of questions should the ontology answer?**
  - What queries will users need to make?
  - What information retrieval needs exist?
  - What reasoning capabilities are required?

- **Who will use and maintain the ontology?**
  - Who are the end users?
  - Who are the domain experts?
  - Who will maintain and update it over time?

### Deliverables:
- Domain definition document
- Scope boundaries
- Competency questions (5-10 key questions the ontology should answer)
- Stakeholder identification

## Step 2: Consider Reusing Existing Ontologies

**Purpose**: Leverage existing work and ensure interoperability.

### Key Questions to Answer:
- **What existing ontologies cover similar domains?**
  - Are there standard vocabularies in your field?
  - What ontologies do similar applications use?
  - Are there industry standards to follow?

- **What ontologies are required for interoperability?**
  - What systems will this ontology interact with?
  - Are there mandated standards or vocabularies?
  - What import/export requirements exist?

- **What can be adapted or extended?**
  - Which existing ontologies can be reused as-is?
  - What needs modification for your use case?
  - What gaps need to be filled with new concepts?

### Deliverables:
- List of relevant existing ontologies
- Reuse strategy document
- Gap analysis
- Import/extension plan

## Step 3: Enumerate Important Terms

**Purpose**: Create a comprehensive vocabulary of domain concepts.

### Key Questions to Answer:
- **What are all the important terms in the domain?**
  - What concepts do domain experts talk about?
  - What terms appear in relevant documents?
  - What vocabulary is used in existing systems?

- **What properties do these terms have?**
  - What attributes describe each concept?
  - What characteristics are important?
  - What metadata is relevant?

- **What relationships exist between terms?**
  - How do concepts relate to each other?
  - What dependencies exist?
  - What hierarchies are apparent?

### Deliverables:
- Comprehensive term list
- Property inventory
- Relationship mapping
- Domain vocabulary document

## Step 4: Define Classes and Class Hierarchy

**Purpose**: Organize concepts into a structured taxonomy.

### Key Questions to Answer:
- **Which terms represent independent objects?**
  - What are the main entity types?
  - What concepts have independent existence?
  - What are the primary classes?

- **What is the hierarchical structure?**
  - What are the "kind-of" relationships?
  - How should classes be organized?
  - What inheritance patterns exist?

- **Which approach works best for your domain?**
  - Top-down: Start with general concepts
  - Bottom-up: Start with specific instances
  - Combination: Start with middle-level concepts

- **Are the class relationships correct?**
  - Does every subclass represent a "kind of" its superclass?
  - Are there any circular dependencies?
  - Do siblings represent concepts at the same level?

### Deliverables:
- Class hierarchy diagram
- Class definitions
- Inheritance relationships
- Hierarchy validation report

## Step 5: Define Properties of Classes

**Purpose**: Specify the attributes and relationships of each class.

### Key Questions to Answer:
- **What properties does each class need?**
  - What intrinsic properties exist?
  - What extrinsic properties are relevant?
  - What parts does each object have?
  - What relationships to other objects exist?

- **Where should properties be attached?**
  - What is the most general class that can have each property?
  - How should properties be inherited?
  - What properties are specific to subclasses?

- **What are the property types?**
  - Object properties (relationships to other objects)
  - Data properties (attributes with literal values)
  - Functional properties (single value)
  - Multi-valued properties

### Deliverables:
- Property definitions for each class
- Property hierarchy
- Domain and range specifications
- Property inheritance rules

## Step 6: Define Property Facets and Constraints

**Purpose**: Specify detailed constraints and value types for properties.

### Key Questions to Answer:
- **What are the cardinality constraints?**
  - How many values can each property have?
  - What are the minimum and maximum cardinalities?
  - Are there required vs. optional properties?

- **What are the value types?**
  - String, Number, Boolean, Date?
  - Enumerated values (specific allowed values)?
  - Instance types (references to other classes)?

- **What are the domain and range restrictions?**
  - Which classes can have each property?
  - What types of values are allowed?
  - Are there specific value constraints?

- **Are there any other constraints?**
  - Value ranges for numeric properties?
  - Pattern constraints for strings?
  - Logical constraints between properties?

### Deliverables:
- Property facet specifications
- Constraint definitions
- Value type mappings
- Validation rules

## Step 7: Create Instances and Test

**Purpose**: Populate the ontology with sample data and validate the design.

### Key Questions to Answer:
- **What are representative instances?**
  - What are good examples of each class?
  - What sample data should be included?
  - How many instances are needed for testing?

- **How do instances relate to each other?**
  - What property values should be filled?
  - What relationships exist between instances?
  - Are there any missing connections?

- **Does the ontology answer competency questions?**
  - Can the sample data answer the original questions?
  - Are there gaps in the knowledge representation?
  - What refinements are needed?

- **Are there any modeling errors?**
  - Do the instances fit the class definitions?
  - Are there logical inconsistencies?
  - What corrections are needed?

### Deliverables:
- Sample instance data
- Test results against competency questions
- Error identification and fixes
- Validation report

## Step 8: Refine and Iterate

**Purpose**: Continuously improve the ontology based on testing and feedback.

### Key Questions to Answer:
- **What issues were discovered during testing?**
  - What modeling problems exist?
  - What concepts are missing?
  - What relationships need adjustment?

- **How can the ontology be improved?**
  - What refinements are needed?
  - What additional concepts should be added?
  - What constraints need adjustment?

- **Is the ontology ready for production?**
  - Does it meet all requirements?
  - Are stakeholders satisfied?
  - Is the documentation complete?

- **What maintenance procedures are needed?**
  - How will the ontology be updated?
  - Who will maintain it?
  - What version control is needed?

### Deliverables:
- Refined ontology
- Updated documentation
- Maintenance procedures
- Version control plan

## Step 9: Document and Deploy

**Purpose**: Create comprehensive documentation and deploy the ontology.

### Key Questions to Answer:
- **What documentation is needed?**
  - User guides for different audiences?
  - Technical specifications?
  - Change management procedures?

- **How will the ontology be deployed?**
  - What systems will use it?
  - What integration is needed?
  - What training is required?

- **How will success be measured?**
  - What metrics indicate success?
  - How will usage be tracked?
  - What feedback mechanisms exist?

### Deliverables:
- Complete documentation suite
- Deployment plan
- Training materials
- Success metrics and monitoring

## Key Principles Throughout the Process

1. **Iterative Development**: Ontology development is necessarily iterative - expect to refine and improve continuously.

2. **Application-Driven**: Design decisions should be guided by the intended applications and use cases.

3. **Domain Expert Involvement**: Engage domain experts throughout the process for validation and feedback.

4. **Consistent Naming**: Establish and follow consistent naming conventions for classes and properties.

5. **Reusability**: Design for reuse and interoperability with existing systems and standards.

6. **Maintainability**: Plan for ongoing maintenance and evolution of the ontology.


This workflow provides a comprehensive, step-by-step approach to ontology development based on the methodology outlined in your document. Each step includes specific questions that need to be answered, helping guide the development process and ensure nothing important is overlooked. The workflow emphasizes the iterative nature of ontology development and the importance of domain expert involvement throughout the process.

## 1. Motivation: Why develop an ontology?

An ontology defines a common vocabulary for researchers who need to share information in a domain. It includes machine-interpretable definitions of basic concepts in the domain and relations among them.

Why would someone want to develop an ontology? Some of the reasons are:

- To share common understanding of the structure of information among people or software agents
- To enable reuse of domain knowledge
- To make domain assumptions explicit
- To separate domain knowledge from the operational knowledge
- To analyze domain knowledge
- To make possible the development of knowledge graphs
- To enable natural language querying or SPARQL queries

Sharing common understanding of the structure of information among people or software agents  is one of the more common goals in developing ontologies 

Enabling reuse of domain knowledge was one of the driving forces behind recent surge in ontology research. For example, models for many different domains need to represent the notion of time. This representation includes the notions of time intervals, points in time, relative measures of time, and so on. If one group of researchers develops such an ontology in detail, others can simply reuse it for their domains. Additionally, if we need to build a large ontology, we can integrate several existing ontologies describing portions of the large domain. We can also reuse a general ontology, such as the UNSPSC ontology, and extend it to describe our domain of interest.

Making explicit domain assumptions underlying an implementation makes it possible to change these assumptions easily if our knowledge about the domain changes. Hard-coding assumptions about the world in programming-language code makes these assumptions not only hard to find and understand but also hard to change, in particular for someone without programming expertise. In addition, explicit specifications of domain knowledge are useful for new users who must learn what terms in the domain mean. 

Separating the domain knowledge from the operational knowledge is another common use of ontologies. We can describe a task of configuring a product from its components according to a required specification and implement a program that does this configuration independent of the products and components themselves (McGuinness and Wright 1998). We can then develop an ontology of PC-components and characteristics and apply the algorithm to configure made-to-order PCs. We can also use the same algorithm to configure elevators if we “feed” an elevator component ontology to it (Rothenfluh et al. 1996).

Analyzing domain knowledge is possible once a declarative specification of the terms is available.  Formal analysis of terms is extremely valuable when both attempting to reuse existing ontologies and extending them (McGuinness et al. 2000).

Often an ontology of the domain is not a goal in itself. Developing an ontology is akin to defining a set of data and their structure for other programs to use. Problem-solving methods, domain-independent applications, and software agents use ontologies and knowledge bases built from ontologies as data. For example, in this paper we develop an ontology of wine and food and appropriate combinations of wine with meals. This ontology can then be used as a basis for some applications in a suite of restaurant-managing tools: One application could create wine suggestions for the menu of the day or answer queries of waiters and customers. Another application could analyze an inventory list of a wine cellar and suggest which wine categories to expand and which particular wines to purchase for upcoming menus or cookbooks.

## About this guide

The wine and food example that we use throughout this guide, is loosely based on an example knowledge base presented in the paper describing CLASSIC—a knowledge-representation system based on a description-logics approach (Brachman et al. 1991). The CLASSIC tutoal (McGuinness et al. 1994) has developed this example further. Protg-2000 and other frame-based systems describe ontologies declaratively, stating explicitly what the class hierarchy is and to which classes individuals belong.

Some ontology-design ideas in this guide originated from the literature on object-oriented design (Rumbaugh et al. 1991; Booch et al. 1997). However, ontology development is different from designing classes and relations in object-oriented programming. Object-oriented programming centers primarily around methods on classes—a programmer makes design decisions based on the operational properties of a class, whereas an ontology designer makes these decisions based on the structural properties of a class. As a result, a class structure and relations among classes in an ontology are different from the structure for a similar domain in an object-oriented program.

Finally, there is no single correct ontology-design methodology and we did not attempt to define one. The ideas that we present here are the ones that we found useful in our own ontology-development experience. At the end of this guide we suggest a list of references for alternative methodologies.

## 2. What is in an ontology?
The Artificial-Intelligence literature contains many definitions of an ontology; many of these contradict one another. For the purposes of this guide an ontology is a formal explicit description of concepts in a domain of discourse (classes (sometimes called concepts)), properties of each concept describing various features and attributes of the concept (properties (sometimes called roles)), and restrictions on properties (facets (sometimes called role restrictions)). An ontology together with a set of individual instances of classes constitutes a knowledge base. In reality, there is a fine line where the ontology ends and the knowledge base begins.

Classes are the focus of most ontologies. Classes describe concepts in the domain. For example, a class of wines represents all wines. Specific wines are instances of this class. The Bordeaux wine in the glass in front of you while you read this document is an instance of  the class of Bordeaux wines. A class can have subclasses that represent concepts that are more specific than the superclass. For example, we can divide the class of all wines into red, white, and rose wines. Alternatively, we can divide a class of all wines into sparkling and non-sparkling wines. 
Properties describe attributes of classes and instances: Chteau Lafite Rothschild Pauillac wine has a full body; it is produced by the Chateau Lafite Rothschild winery. We have two properties describing the wine in this example: the property body with the value full and the property maker with the value Chateau Lafite Rothschild winery. At the class level, we can say that instances of the class Wine will have properties describing their flavor, body, sugar level, the maker of the wine and so on.[1]

All instances of the class Wine, and its subclass Pauillac, have a property maker the value of which is an instance of the class Winery (Figure 1). All instances of the class Winery have a property produces that refers to all the wines (instances of the class Wine and its subclasses) that the winery produces.

In practical terms, developing an ontology includes:

- defining classes in the ontology
- arranging the classes in a taxonomic (subclass–superclass) hierarchy
- defining properties and describing allowed values for these properties
- filling in the values for properties for sample instances

We can then create a knowledge base by defining individual instances of these classes filling in specific property value information and additional property restrictions.

## 3. A Simple Knowledge-Engineering Methodology
There is no one “correct” way or methodology for developing ontologies. Here we discuss general issues to consider and offer one possible process for developing an ontology. We describe an iterative approach to ontology development: we start with a rough first pass at the ontology. We then revise and refine the evolving ontology and fill in the details. Along the way, we discuss the modeling decisions that a designer needs to make, as well as the pros, cons, and implications of different solutions.

First, we would like to emphasize some fundamental rules in ontology design to which we will refer many times. These rules may seem rather dogmatic. They can help, however, to make design decisions in many cases.
1. There is no one correct way to model a domain— there are always viable alternatives. The best solution almost always depends on the application that you have in mind and the extensions that you anticipate.
2. Ontology development is necessarily an iterative process.
3. Concepts in the ontology should be close to objects (physical or logical) and relationships in your domain of interest. These are most likely to be nouns (objects) or verbs (relationships) in sentences that describe your domain.

That is, deciding what we are going to use the ontology for, and how detailed or general the ontology is going to be will guide many of the modeling decisions down the road. Among several viable alternatives, we will need to determine which one would work better for the projected task, be more intuitive, more extensible, and more maintainable. We also need to remember that an ontology is a model of reality of the world and the concepts in the ontology must reflect this reality. After we define an initial version of the ontology, we can evaluate and debug it by using it in applications or problem-solving methods or by discussing it with experts in the field, or both. As a result, we will almost certainly need to revise the initial ontology. This process of iterative design will likely continue through the entire lifecycle of the ontology.

### Step 1. Determine the domain and scope of the ontology

We suggest starting the development of an ontology by defining its domain and scope. That is, answer several basic questions:
- What is the domain that the ontology will cover?
- For what we are going to use the ontology?
- For what types of questions the information in the ontology should provide answers?
- Who will use and maintain the ontology?

Consider the ontology of wine and food that we introduced earlier. Representation of food and wines is the domain of the ontology. We plan to use this ontology for the applications that suggest good combinations of wines and food.

Naturally, the concepts describing different types of wines, main food types, the notion of a good combination of wine and food and a bad combination will figure into our ontology. At the same time, it is unlikely that the ontology will include concepts for managing inventory in a winery or employees in a restaurant even though these concepts are somewhat related to the notions of wine and food.

If the ontology we are designing will be used to assist in natural-language processing of articles in wine magazines, it may be important to include synonyms and part-of-speech information for concepts in the ontology. If the ontology will be used to help restaurant customers decide which wine to order, we need to include retail-pricing information.  If it is used for wine buyers in stocking a wine cellar, wholesale pricing and availability may be necessary.  If the people who will maintain the ontology describe the domain in a language that is different from the language of the ontology users, we may need to provide the mapping between the languages.

#### Competency questions
One of the ways to determine the scope of the ontology is to sketch a list of questions that a knowledge base based on the ontology should be able to answer, competency questions (Gruninger and Fox 1995). These questions will serve as the litmus test later: 
- Does the ontology contain enough information to answer these types of questions? 
- Do the answers require a particular level of detail or representation of a particular area? 
These competency questions are just a sketch and do not need to be exhaustive.

In the wine and food domain, the following are the possible competency questions:
- Which wine characteristics should I consider when choosing a wine?
- Is Bordeaux a red or white wine?
- Does Cabernet Sauvignon go well with seafood?
- What is the best choice of wine for grilled meat?
- Which characteristics of a wine affect its appropriateness for a dish?
- Does a bouquet or body of a specific wine change with vintage year?
- What were good vintages for Napa Zinfandel?

Judging from this list of questions, the ontology will include the information on various wine characteristics and wine types, vintage years—good and bad ones—classifications of foods that matter for choosing an appropriate wine, recommended combinations of wine and food.

### Step 2. Consider reusing existing ontologies

It is almost always worth considering what someone else has done and checking if we can refine and extend existing sources for our particular domain and task. Reusing existing ontologies may be a requirement if our system needs to interact with other applications that have already committed to particular ontologies or controlled vocabularies.  Many ontologies are already available in electronic form and can be imported into an ontology-development environment that you are using. The formalism in which an ontology is expressed often does not matter, since many knowledge-representation systems can import and export ontologies. Even if a knowledge-representation system cannot work directly with a particular formalism, the task of translating an ontology from one formalism to another is usually not a difficult one.

There are many widely-used ontologies that can be considered for reuse. Here are some of the most popular ones:

- **Dublin Core Terms (dterms)** - Metadata terms for resource description
  - Prefix: `dct:` or `dcterms:`
  - Namespace: http://purl.org/dc/terms/
  - Used for: Document and resource metadata like title, creator, date, etc.

- **FOAF (Friend of a Friend)** - Describing people and their relationships
  - Prefix: `foaf:`
  - Namespace: http://xmlns.com/foaf/0.1/
  - Used for: People, organizations, and social networks

- **Schema.org** - General purpose vocabulary for structured data
  - Prefix: `schema:` 
  - Namespace: https://schema.org/
  - Used for: Products, events, organizations, creative works, etc.

- **PROV-O** - Provenance Ontology
  - Prefix: `prov:`
  - Namespace: http://www.w3.org/ns/prov#
  - Used for: Representing provenance information

- **DCAT** - Data Catalog Vocabulary
  - Prefix: `dcat:`
  - Namespace: http://www.w3.org/ns/dcat#
  - Used for: Describing datasets in data catalogs

- **FIBO** - Financial Industry Business Ontology
  - Prefix: `fibo:`
  - Namespace: https://spec.edmcouncil.org/fibo/
  - Used for: Financial instruments, processes and entities

- **DPROD** - Data Product Ontology
  - Prefix: `dprod:`
  - Namespace: http://dprod.org/ontology#
  - Used for: Describing data products and their characteristics

These ontologies are well-maintained, widely adopted, and follow best practices in ontology engineering. When possible, it's recommended to reuse terms from these established ontologies rather than creating new ones, as this promotes interoperability and reduces redundancy in the semantic web ecosystem.


### Step 3. Enumerate important terms in the ontology

It is useful to write down a list of all terms we would like either to make statements about or to explain to a user. What are the terms we would like to talk about? What properties do those terms have? What would we like to say about those terms? For example, important wine-related terms will include wine, grape, winery, location, a wine’s color, body, flavor and sugar content; different types of food, such as fish and red meat; subtypes of wine such as white wine, and so on. Initially, it is important to get a comprehensive list of terms without worrying about overlap between concepts they represent, relations among the terms, or any properties that the concepts may have, or whether the concepts are classes or properties.

The next two steps—developing the class hierarchy and defining properties of concepts (slots)—are closely intertwined. It is hard to do one of them first and then do the other. Typically, we create a few definitions of the concepts in the hierarchy and then  continue by describing properties of these concepts and so on. These two steps are also the most important  steps in the ontology-design process. We will describe them here briefly and then spend the next two sections discussing the more complicated issues that need to be considered, common pitfalls, decisions to make, and so on.

### Step 4. Define the classes and the class hierarchy

There are several possible approaches in developing a class hierarchy 

- A top-down development process starts with the definition of the most general concepts in the domain and subsequent specialization of the concepts. For example, we can start with creating classes for the general concepts of Wine and Food. Then we specialize the Win class by creating some of its subclasses: White wine, Red wine, Ros wine. We can further categorize the Red wine class, for example, into Syrah, Red Burgundy, Cabernet Sauvignon, and so on.

- A bottom-up development process starts with the definition of the most specific classes, the leaves of the hierarchy, with subsequent grouping of these classes into more general concepts. For example, we start by defining classes for Pauillac and Margaux wines. We then create a common superclass for these two classes—Medoc—which in turn is a subclass of Bordeaux.

- A combination development process is a combination of the top-down and bottom-up approaches: We define the more salient concepts first and then generalize and specialize them appropriately. We might start with a few top-level concepts such as Wine, and a few specific concepts, such as Margaux . We can then relate them to a middle-level concept, such as Medoc.  Then we may want to generate all of the regional wine classes from France, thereby generating a number of middle-level concepts.

None of these three methods is inherently better than any of the others. The approach to take depends strongly on the personal view of the domain. If a developer has a systematic top-down view of the domain, then it may be easier to use the top-down approach. The combination approach is often the easiest for many ontology developers, since the concepts “in the middle” tend to be the more descriptive concepts in the domain (Rosch 1978).

If you tend to think of wines by distinguishing the most general classification first, then the top-down approach may work better for you. If you’d rather start by getting grounded with specific examples, the bottom-up approach may be more appropriate.

Whichever approach we choose, we usually start by defining classes. From the list created in Step 3, we select the terms that describe objects having independent existence rather than terms that describe these objects. These terms will be classes in the ontology and will become anchors in the class hierarchy.[2] We organize the classes into a hierarchical taxonomy by asking if by being an instance of one class, the object will necessarily (i.e., by definition) be an instance of some other class.

If a class A is a superclass of class B, then every instance of B is also an instance of A

In other words, the class B represents a concept that is a “kind In other words, the class B represents a concept that is a “kind of” A.

For example, every Pinot Noir wine is necessarily a red wine. Therefore the Pinot  Noir class is a subclass of the Red Wine class.

### Step 5. Define the properties of classes

The classes alone will not provide enough information to answer the competency questions from Step 1. Once we have defined some of the classes, we must describe the internal structure of concepts.

We have already selected classes from the list of terms we created in Step 3. Most of the remaining terms are likely to be properties of these classes. These terms include, for example, a wine’s color, body, flavor and sugar content and location of a winery.

For each property in the list, we must determine which class it describes. These properties become properties attached to classes. Thus, the Wine class will have the following properties: color,  body, flavor, and sugar. And the class Winery will have a location property.

In general, there are several types of object properties that can become properties in an ontology:

- **"intrinsic" properties** such as the flavor of a wine
- **"extrinsic" properties** such as a wine's name, and area it comes from
- **parts**, if the object is structured; these can be both physical and abstract "parts" (e.g., the courses of a meal)
- **relationships to other individuals**; these are the relationships between individual members of the class and other items (e.g., the maker of a wine, representing a relationship between a wine and a winery, and the grape the wine is made from.)

Thus, in addition to the properties we have identified earlier, we need to add the following properties to the Wine class: name, area, maker, grape. Figure 3 shows the properties for the class Wine.

All subclasses of a class inherit the properties of that class. For example, all the properties of the class Wine will be inherited to all subclasses of Wine, including Red Wine and White Wine. We will add an additional property, tannin level (low, moderate, or high), to the Red Wine class. The tannin level property will be inherited by all the classes representing red wines (such as Bordeaux and Beaujolais).

A property should be attached at the most general class that can have that property. For instance, body and color of a wine should be attached at the class Wine, since it is the most general class whose instances will have body and color. 

### Step 6. Define the facets of the properties

Properties can have different facets describing the value type, allowed values, the number of the values (cardinality), and other features of the values the property can take. For example, the value of a name property (as in "the name of a wine") is one string. That is, name is a property with value type String. A property produces (as in "a winery produces these wines") can have multiple values and the values are instances of the class Wine. That is, produces is a property with value type Instance with Wine as allowed class.

We will now describe several common facets.

#### Property cardinality

Property cardinality defines how many values a property can have. Some systems distinguish only between single cardinality (allowing at most one value) and multiple cardinality (allowing any number of values). A body of a wine will be a single cardinality property (a wine can have only one body). Wines produced by a particular winery fill in a multiple-cardinality property produces for a Winery class.

Some systems allow specification of a minimum and maximum cardinality to describe the number of property values more precisely. Minimum cardinality of N means that a property must have at least N values. For example, the grape property of a Wine has a minimum cardinality of 1: each wine is made of at least one variety of grape. Maximum cardinality of M means that a property can have at most M values. The maximum cardinality for the grape property for single varietal wines is 1: these wines are made from only one variety of grape. Sometimes it may be useful to set the maximum cardinality to 0. This setting would indicate that the property cannot have any values for a particular subclass.

#### Property-value type
A value-type facet describes what types of values can fill in the property. Here is a list of the more common value types:

- String is the simplest value type which is used for properties such as name: the value is a simple string

- Number (sometimes more specific value types of Float and Integer are used) describes properties with numeric values. For example, a price of a wine can have a value type Float

- Boolean properties are simple yes–no flags. For example, if we choose not to represent sparkling wines as a separate class, whether or not a wine is sparkling can be represented as a value of a Boolean property: if the value is "true" ("yes") the wine is sparkling and if the value is "false" ("no") the wine is not a sparkling one.

- Enumerated properties specify a list of specific allowed values for the property. For example, we can specify that the flavor property can take on one  the three possible values: strong, moderate, and delicate. In Protg-2000 the enumerated properties are of type Symbol.

- Instance-type properties allow definition of relationships between individuals. Properties with value type Instance must also define a list of allowed classes from which the instances can come. For example, a property produces for the class Winery may have instances of the class Wine as its values.[3]

#### Domain and range of a property
Allowed classes for properties of type Instance are often called a range of a property. In the example in Figure 4 the class Wine is the range of the produces property. Some systems allow restricting the range of a property when the property is attached for a particular class.

The classes to which a property is attached or a classes which property a property describes, are called the domain of the property. The Winery class is the domain of the produces property. In the systems where we attach properties to classes, the classes to which the property is attached usually constitute the domain of that property. There is no need to specify the domain separately.

The basic rules for determining a domain and a range of a property are similar:

When defining a domain or a range for a property, find the most general classes or class that can be respectively the domain or the range for the properties .

On the other hand, do not define a domain and range that is overly general: all the classes in the domain of a property should be described by the property and instances of all the classes in the range of a property should be potential fillers for the property. an overly general class for range (i.e., one would not want to make the range THING) but one would want to choose a class that will cover all fillers

Instead of listing all possible subclasses of the Wine class for the range of the produces property, just list Wine. At the same time, we do not want to specify the range of the property as THING—the most general class in an ontology.

In more specific terms:

If a list of classes defining a range or a  domain of a property includes a class and its subclass, remove the subclass.

If the range of the property contains both the Wine class and the Red Wine class, we can remove the Red Wine from the range because it does not add any new information: The Red Wine is a subclass of Wine and therefore the property range already implicitly includes it as well as all other subclasses of the Wine class.

If a list of classes defining a range or a  domain of a property contains all subclasses of a class A, but not the class A itself, the range should contain only the class A and not the subclasses.

Instead of defining the range of the property to include Red Wine, White Wine, and Rose Wine (enumerating all the direct subclasses of Wine), we can limit the range to the class Wine itself.

If a list of classes defining a range or a  domain of a property contains all but a few subclasses of a class A, consider if the class A would make a more  appropriate range definition.

In systems where attaching a property to a class is the same as adding the class to the domain of the property, the same rules apply to property attachment: On the one hand, we should try to make it as general as possible. On the other hand, we must ensure that each class to which we attach the property can indeed have the property that the property represents. We can attach the tannin level property to each of the classes representing red wines (e.g., Bordeaux, Merlot, Beaujolais, etc.). However, since all red wines have the tannin-level property, we should instead attach the property to this more general class of Red Wines. Generalizing the domain of the tannin level property further (by attaching it to the Wine class instead) would not be correct since we do not use tannin level to describe white wines for example.

### Step 7. Create instances

The last step is creating individual instances of classes in the hierarchy. Defining an individual instance of a class requires (1) choosing a class, (2) creating an individual instance of that class, and (3) filling in the property values. For example, we can create an individual instance Chateau-Morgon-Beaujolais to represent a specific type of Beaujolais wine. Chateau-Morgon-Beaujolais is an instance of the class Beaujolais representing all Beaujolais wines. This instance has the following property values defined (Figure 5):

- **Body:** Light
- **Color:** Red
- **Flavor:** Delicate
- **Tannin level:** Low
- **Grape:** Gamay (instance of the Wine grape class)
- **Maker:** Chateau-Morgon (instance of the Winery class)
- **Region:** Beaujolais (instance of the Wine-Region class)
- **Sugar:** Dry


Figure 5. The definition of an instance of the Beaujolais class. The instance is Chateua Morgon Beaujolais from the Beaujolais region, produced from the Gamay grape by the Chateau Morgon winery. It has a light body, delicate flavor, red color, and low tannin level. It is a dry wine.

## 4. Defining classes and a class hierarchy
This section discussed things to look out for and errors that are easy to make when defining classes and a class hierarchy (Step 4 from Section 3). As we have mentioned before, there is no single correct class hierarchy for any given domain. The hierarchy depends on the possible uses of the ontology, the level of the detail that is necessary for the application, personal preferences, and sometimes requirements for compatibility with other models. However, we discuss several guidelines to keep in mind when developing a class hierarchy. After defining a considerable number of new classes, it is helpful to stand back and check if the emerging hierarchy conforms to these guidelines.

### 4.1 Ensuring that the class hierarchy is correct
An “is-a” relation
The class hierarchy represents an “is-a” relation: a class A is a subclass of B if every instance of B is also an instance of A. For example, Chardonnay is a subclass of White wine. Another way to think of the taxonomic relation is as a “kind-of” relation: Chardonnay is a kind of White wine. A jetliner is a kind of an aircraft. Meat is a kind of food.

A subclass of a class represents a concept that is a “kind of” the concept that the superclass represents.

A single wine is not a subclass of all wines
A common modeling mistake is to include both a singular and a plural version of the same concept in the hierarchy making the former a subclass of the latter. For example, it is wrong to define a class Wines and a class Wine as a subclass of Wines. Once you think of the hierarchy as representing the “kind-of” relationship, the modeling error becomes clear: a single Wine is not a kind of Wines. The best way to avoid such an error is always to use either singular or plural in naming classes (see Section 6 for the discussion on naming concepts).

Transitivity of the hierarchical relations
A subclass relationship is transitive:

If B is a subclass of A and C is a subclass of B, then C is a subclass of A

For example, we can define a class Wine, and then define a class White wine as a subclass of Wine. Then we define a class Chardonnay as a subclass of White wine. Transitivity of the subclass relationship means that the class Chardonnay is also a subclass of Wine. Sometimes we distinguish between direct subclasses and indirect subclasses. A direct subclass is the “closest” subclass of the class: there are no classes between a class and its direct subclass in a hierarchy. That is, there are no other classes in the hierarchy between a class and its direct superclass. In our example, Chardonnay is a direct subclass of White wine and is not a direct subclass of Wine.

Evolution of a class hierarchy
Maintaining a consistent class hierarchy may become challenging as domains evolve. For example, for many years, all Zinfandel wines were red. Therefore, we define a class of Zinfandel wines as a subclass of the Red wine class. Sometimes, however, wine makers began to press the grapes and to take away the color-producing aspects of the grapes immediately, thereby modifying the color of the resulting wine. Thus, we get “white zinfandel” whose color is rose. Now we need to break the Zinfandel class into two classes of zinfandel—White zinfandel and Red zinfandel—and classify them as subclasses of Rose wine and Red wine respectively. 

Classes and their names
It is important to distinguish between a class and its name:

Classes represent concepts in the domain and not the words that denote these concepts.

The name of a class may change if we choose a different terminology, but the term itself represents the objective reality in the world. For example, we may create a class Shrimps, and then rename it to Prawns—the class still represents the same concept. Appropriate wine combinations that referred to shrimp dishes should refer to prawn dishes. In more practical terms, the following rule should always be followed:

Synonyms for the same concept do not represent different classes

Synonyms are just different names for a concept or a term. Therefore, we should not have a class called Shrimp and a class called Prawn, and, possibly a class called Crevette. Rather, there is one class, named either Shrimp or Prawn. Many systems allow associating a list of synonyms,  translations, or presentation names with a class. If a system does not allow this associations, synonyms could always be listed in the class documentation.

Avoiding class cycles
We should avoid cycles in the class hierarchy. We say that there is a cycle in a hierarchy when some class A has a subclass B and at the same time B is a superclass of A. Creating such a cycle in a hierarchy amounts to declaring that the classes A and B are equivalent: all instances of A are instances of B and all instances of B are also instances of A. Indeed, since B is a subclass of A, all B’s instances must be instances of the class A. Since A is a subclass of B, all A’s instances must also be instances of the class B.

### 4.2 Analyzing siblings in a class hierarchy
Siblings in a class hierarchy
Siblings in the hierarchy are classes that are direct subclasses of the same class (see Section 4.1).

All the siblings in the hierarchy (except for the ones at the root) must be at the same level of generality.

For example, White wine and Chardonnay should not be subclasses of the same class (say, Wine). White wine is a more general concept than Chardonnay. Siblings should represent concepts that fall “along the same line” in the same way that  same-level sections in a book are at the same level of generality. In that sense, requirements for a class hierarchy are similar to the requirements for a book outline.

The concepts at the root of the hierarchy however (which are often represented as direct subclasses of some very general class, such as Thing) represent major divisions of the domain and do not have to be similar concepts.

How many is too many and how few is too few?
There are no hard rules for the number of direct subclasses that a class should have. However, many well structured ontologies have between two and a dozen direct subclasses. Therefore, the following two guidelines:

If a class has only one direct subclass there may be a modeling problem or the ontology is not complete.

If there are more than a dozen subclasses for a given class then additional intermediate categories may be necessary.

The first of the two rules is similar to a typesetting rule that bulleted lists should never have onl one bullet point. For example, most of the red Burgundy wines are Ctes d’Or wines. Suppose we wanted to represent only this majority type of Burgundy wines. We could create a class Red Burgundy and then a single subclass Cotes d’Or(Figure 6a). However, if in our representation red Burgundy and Ctes dOr wines are essentiall equivalent (all red Burgundy wines are Ctes d’Or wines and all Ctes d’Or wines are red Burgundy wines), creating the Cotes d’Or class is not necessary and does not ad any new information to the representation. If we were to include Ctes Chalonnaise wins, which are cheaper Burgundy wines from the region just South of Ctes d’Or, then we will create two subclasses of the Burgundy class: Cotes d’Or and Cotes Chalonnaise (Figure 6b).


Suppose now that we list all types of wines as direct subclasses of the Wine class. This list would then include such more general types of wine as Beaujolais and Bordeaux, as well as more specific types such as Paulliac and Margaux (Figure 7a). The class Wine has too many direct subclasses and, indeed, for the ontology to reflect the different types of wine in a more organized manner, Medoc should be a subclass of Bordeaux and Cotes d’Or should be a subclass of Burgundy. Also having such intermediate categories as Red wine and White wine would also reflect the conceptual model of the domain of wines that many people have (Figure 7b).

However, if no natural classes exist to group concepts in the long list of siblings, there is no need to create artificial classes—just leave the classes the way they are. After all, the ontology is a reflection of the real world, and if no categorization exists in the real world, then the ontology should reflect that.


Figure 7. Categorizing wines. Having all the wines and types of wine versus having several levels of categorization.

### 4.3 Multiple inheritance
Most knowledge-representation systems allow multiple inheritance in the class hierarchy: a class can be a subclass of several classes. Suppose we would like to create a separate class of dessert wines, the Dessert wine class. The Port wine is both a red wine and a dessert wine.[4] Therefore, we define a class Port to have two superclasses: Red wine and Dessert wine. All instances of the Port class will be instances of both the Red wine class and the Dessert wine class. The Port class will inherit its properties and their facets from both its parents. Thus, it will inherit the value SWEET for the property Sugar from the Dessert wine class and the tannin level property and the value for its color property from the Red wine class.

### 4.4 When to introduce a new class (or not)
One of the hardest decisions to make during modeling is when to introduce a new class or when to represent a distinction through different property values. It is hard to navigate both an extremely nested hierarchy with many extraneous classes and a very flat hierarchy that has too few classes with too much information encoded in properties. Finding the appropriate balance though is not easy.

There are several rules of thumb that help decide when to introduce new classes in a hierarchy.

Subclasses of a class usually (1) have additional properties that the superclass does  not have, or (2) restrictions different from those of the superclass, or (3) participate in different relationships than the superclasses

Red wines can have different levels of tannin, whereas this property is not used to describe wines in general. The value for the sugar property of the Dessert wine is SWEET, whereas it is not true of the superclass of the Dessert Wine class. Pinot Noir wines may go well with seafood whereas other red wines do not. In other words, we introduce a new class in the hierarchy usually only when there is something that we can say about this class that we cannot say about the superclass.

In practical terms, each subclass should either have new properties added to it, or have new property values defined, or override some facets for the inherited properties.

However, sometimes it may be useful to create new classes even if they do not introduce any new properties.

Classes in terminological hierarchies do not have to introduce new properties

For example, some ontologies include large reference hierarchies of common terms used in the domain. For example, an ontology underlying an electronic medical-record system may include a classification of various diseases. This classification may be just that—a hierarchy of terms, without properties (or with the same set of properties). In that case, it is still useful to organize the terms in a hierarchy rather than a flat list because it will (1) allow easier exploration and navigation and (2) enable a doctor to choose easily a level of generality of the term that is appropriate for the situation.

Another reason to introduce new classes without any new properties is to model concepts among which domain experts commonly make a distinction even though we may have decided not to model the distinction itself. Since we use ontologies to facilitate communication among domain experts and between domain experts and knowledge-based systems we would like to reflect the expert’s view of the domain in the ontology.

Finally, we should not create subclasses of a class for each additional restriction.  For example, we introduced the classes Red wine, White wine, and Rose wine  because this distinction is a natural one in the wine world. We did not introduce classes  for delicate wine, moderate wine, and so on. When defining a class hierarchy, our goal is to strike a balance between creating new classes useful for class organization and creating too many classes.

### 4.5 A new class or a property value?
When modeling a domain, we often need to decide hether to model a specific distinction (such as white, red, or ros wine) as a property value or as a set of classes again depends on the scope of the domain and the task at hand. 

Do we create a class White wine or do we simply create a class Wine and fill in different values for the property color? The answer usually lies in the scope that we defined for the ontology. How important the concept of White wine is in our domain? If wines have only marginal importance in the domain and whether or not the wine is white does not have any particular implications for its relations to other objects, then we shouldn't introduce a separate class for white wines. For a domain model used in a factory producing wine labels, rules for wine labels of any color are the same and the distinction is not very important. Alternatively, for the representation of wine, food, and their appropriate combinations a red wine is very different from a white wine: it is paired with different foods, has different properties, and so on. Similarly, color of wine is important for the wines knowledge base that we may use to determine wine-tasting order.  Thus, we create a separate class for White wine.

If the concepts with different property values become restrictions for different properties in other classes. Otherwise, we represent the distinction in a property value.

Similarly, our wine ontology has such classes as Red Merlot and White Merlot, rather than a single class for all Merlot wines: red Merlots and white Merlots are really different wines (made from the same grape) and if we are developing a detailed ontology of wine, this distinction is important.

If a distinction is important in the domain and we think of the objects with different values for the distinction as different kinds of objects,  then we should create a new class for the distinction.

Considering potential individual instances of a class may also be helpful in deciding whether or not to introduce a new class.

A class to which an individual instance belongs should not change often.

Usually when we use extrinsic rather than intrinsic properties of concepts to differentiate among classes, instances of those classes will have to migrate often from one class to another. For example, Chilled wine should not be a class in an ontology describing wine bottles in a restaurant. The property chilled should simply be an attribute of wine in a bottle since an instance of Chilled wine can easily cease being an instance of this class and then become an instance of this class again.

Usually numbers, colors, locations are property values and do not cause the creation of new classes. Wine, however, is a notable exception since the color of the wine is so paramount to the description of wine.

For another example, consider the human-anatomy ontology. When we represent ribs, do we create a class for each of the "1st left rib", "2nd left rib", and so on? Or do we have a class Rib with properties for the order and the lateral position (left-right)?[5] If the information about each of the ribs that we represent in the ontology is significantly different, then we should indeed create a class for each of the ribs. That is, if we want to represent details adjacency and location information (which is different for each rib) as well as specific functions that each rib playa and organs it protects, we want the classes. If we are modeling anatomy at a slightly lesser level of generality, and all ribs are very similar as far as our potential applications are concerned (we just talk about which rib is broken on the X-Ray without implications for other parts of the body), we may want to simplify our hierarchy and have just the class Rib, with two properties: lateral position, order.

### 4.6 An instance or a class?
Deciding whether a particular concept is a class in an ontology or an individual instance depends on what the potential applications of the ontology are. Deciding where classes end and individual instances begin starts with deciding what is the lowest level of granularity in the representation. The level of granularity is in turn determined by a potential application of the ontology. In other words, what are the most specific items that are going to be represented in the knowledge base? Going back to the competency questions we identified in Step 1 in Section 3, the most specific concepts that will constitute answers to those questions are very good candidates for individuals in the knowledge base.

Individual instances are the most specific concepts represented in a knowledge base.

For example, if we are only going to talk about pairing wine with food we will not be interested in the specific physical bottles of wine. Therefore, such terms as Sterling Vineyards Merlot are probably going to be the most specific terms we use. Therefore, Sterling Vineyards Merlot would be an instance in the knowledge base.

On the other hand, if we would like to maintain an inventory of wines in the restaurant in addition to the knowledge base of good wine-food pairings, individual bottles of each wine may become individual instances in our knowledge base.

Similarly, if we would like to record different properties for each specific vintage of the Sterling Vineyards Merlot, then the specific vintage of the wine is an instance in a knowledge base and Sterling Vineyards Merlot is a class containing instances for all its vintages.

Another rule can “move” some individual instances into the set of classes:

If concepts form a natural hierarchy, then we should represent them as classes

Consider the wine regions. Initially, we may define main wine regions, such as France, United States, Germany, and so on, as classes and specific wine regions within these large regions as instances. For example, Bourgogne region is an instance of the French region class. However, we would also like to say that the Cotes d’Or region is a Bourgogne region. Therefore, Bourgogne region must be a class (in order to have subclasses or instances). However, making Bourgogne region a class and Cotes d’Or region an instance of Bourgogne region seems arbitrary: it is very hard to clearly distinguish which regions are classes and which are inances. Therefore, we define all wine regions as classes. Protg-2000 allows users to specify some classes as Abstract, signifying that the class cannot have any direct instances. In our case, all region classes are abstract (Figure 8).

The same class hierarchy would be incorrect if we omitted the word “region” from the class names. We cannot say that the class Alsace is a subclass of the class France: Alsace is not a kind of France. However, Alsace region is a kind of a French region.

Only classes can be arranged in a hierarchy—knowledge-representation systems do not have a notion of sub-instance. Therefore, if there is a natural hierarchy among terms, such as in terminological hierarchies from Section 4.2, we should define these terms as classes even though they may not have any instances of their own.

### 4.7 Limiting the scope
As a final note on defining a class hierarchy, the following set of rules is always helpful in deciding when an ontology definition is complete:

The ontology should not contain all the possible information about the domain: you do not need to specialize (or generalize) more than you need for your application (at most one extra level each way).

For our wine and food example, we do not need to know what paper is used for the labels or how to cook shrimp dishes.

Similarly, the ontology should not contain all the possible properties of and distinctions among classes in the hierarchy.

In our ontology, we certainly do not include all the properties that a wine or food could have.  We represented the most salient properties of the classes of items in our ontology.  Even though wine books would tell us the size of grapes, we have not included this knowledge.  Similarly, we have not added all relationships that one could imagine among all the terms in our system.  For example, we do not include relationships such as favorite wine and favorite food in the ontology just to allow a more complete representation of all of the interconnections between the terms we have defined.

The last rules also applies to establishing relations among concepts that we have already included in the ontology. Consider an ontology describing biology experiments. The ontology will likely contain a concept of Biological organisms. It will also contain a concept of an Experimenter performing an experiment (with his name, affiliation, etc.). It is true that an experimenter, as a person, also happens to be a biological organism. However, we probably should not incorporate this distinction in the ontology: for the purposes of this representation an experimenter is not a biological organism and we will probably never conduct experiments on the experimenters themselves. If we were representing everything we can say about the classes in the ontology, an Experimenter would become a subclass of Biological Organism. However, we do not need to include this knowledge for the foreseeable applications. In fact, including this type of additional classification for existing classes actually hurts: now an instance of an Experimenter will have properties for weight, age, species, and other data pertaining to a  biological organism, but absolutely irrelevant in the context of describing an experiment. However, we should record such design decision in the documentation for the benefit of the users who will be looking at this ontology and who may not be aware of the application we had in mind.

### 4.8 Disjoint subclasses
Many systems allow us to specify explicitly that several classes are disjoint. Classes are disjoint if they cannot have any instances in common. For example, the Dessert wine and the White wine  classes in our ontology are not disjoint: there are many wines that are instances of both. The Rothermel Trochenbierenauslese Riesling instance of the Sweet Riesling class is one such example. At the same time, the Red wine and the White wine classes are disjoint: no wine can be simultaneously red and white. Specifying that classes are disjoint  enables the system to validate the ontology better. If we declare the Red wine and the White wine classes to be disjoint and later create a class that is a subclass of both Riesling (a subclass of White wine) and Port (a subclass of Red wine), a system can indicate that there is a modeling error.

## 5. Defining properties—more details
In this section we discuss several more details to keep in mind when defining properties in the ontology (Step 5 and Step 6 in Section 3). Mainly, we discuss inverse properties and default values for a property.

### 5.1 Inverse properties
A value of a property may depend on a value of another property. For example, if a wine was produced by a winery, then the winery produces that wine. These two relations, maker and produces, are called inverse relations. Storing the information "in both directions" is redundant. When we know that a wine is produced by a winery, an application using the knowledge base can always infer the value for the inverse relation that the winery produces the wine. However, from the knowledge-acquisition perspective it is convenient to have both pieces of information explicitly available. This approach allows users to fill in the wine in one case and the winery in another.. The knowledge-acquisition system could then automatically fill in the value for the inverse relation insuring consistency of the knowledge base.

Our example has a pair of  inverse properties: the maker property of the Wine class and the produces property of the Winery class. When a user creates an instance of the Wine class and fills in the value for the maker property, the system automatically adds the newly created instance to the produces property of the corresponding Winery instance. For instance, when we say that Sterling Merlot is produced by the Sterling Vineyard winery, the system would automatically add Sterling Merlot to the list of wines that the Sterling Vineyard winery produces. (Figure 9).


Figure 9. Instances with inverse properties. The property produces for the class Winery is an inverse of the property  maker for the class Wine. Filling in one of the properties triggers an automatic update of the other.

### 5.2 Default values
Many frame-based systems allow specification of default values for properties.  If a particular property value is the same for most instances of a class, we can define this value to be a default value for the property. Then, when each new instance of a class containing this property is created, the system fills in the default value automatically. We can then change the value to any other value that the facets will allow. That is, default values are there for convenience: they do not enforce any new restrictions on the model or change the model in any way.

For example, if the majority of wines we are going to discuss are full-bodied wines, we can have "full" as a default value for the body of the wine. Then, unless we say otherwise, all wines we define would be full-bodied.

Note that this is different from property values. Property values cannot be changed. For example, we can say that the property sugar has value SWEET for the Dessert wine class. Then all the subclasses and instances of the Dessert wine class will have the SWEET value for the property sugar. This value cannot be changed in any of the subclasses or instances of the class.

## 6. What's in a name?
Defining naming conventions for concepts in an ontology and then strictly adhering to these conventions not only makes the ontology easier to understand but also helps avoid some common modeling mistakes. There are many alternatives in naming concepts. Often there is no particular reason to choose one or another alternative. However, we need to

Define a naming convention for classes and properties and adhere to it.

The following features of a knowledge representation system affect the choice of naming conventions:
- Does the system have the same name space for classes, properties, and instances? That is, does the system allow having a class and a property with the same name (such as a class winery and a property winery)?
- Is the system case-sensitive? That is, does the system treat the names that differ only in case as different names (such as Winery and winery)?
- What delimiters does the system allow in the names? That is, can names contain spaces, commas, asterisks, and so on?
Protg-2000, for example, maintains a single name space for all its frames. It is case-sensitive. Thus, we cannot have a class winery and a property winery. We can, however, have a class Winery (not the upper-case) and a property winery. CLASSIC, on the other hand, is not case sensitive and maintains different name spaces for classes, properties, and individuals. Thus, from a system perspective, there is no problem in naming both a class and a property Winery.

### 6.1 Capitalization and delimiters
First, we can greatly improve the readability of an ontology if we use consistent capitalization for concept names. For example, it is common to capitalize class names and use lower case for property names (assuming the system is case-sensitive).

When a concept name contains more than one word (such as Meal course) we need to delimit the words. Here are some possible choices.
- Use Space: Meal course (many systems, including Protg, allow spaces in concept names). 
- Run the words together and capitalize each new word: MealCourse
- Use an underscore or dash or other delimiter in the name: Meal_Course, Meal_course, Meal-Course, Meal-course. (If you use delimiters, you will also need to decide whether or not each new word is capitalized)

If the knowledge-representation system allows spaces in names, using them may be the most intuitive solution for many ontology developers. It is however, important to consider other systems with which your system may interact.  If those systems do not use spaces or if your presentation medium does not handle spaces well, it can be useful to use another method.

### 6.2 Singular or plural
A class name represents a collection of objects. For example, a class Wine actually represents all wines. Therefore, it could be more natural for some designers to call the class Wines rather than Wine. No alternative is better or worse than the other (although singular for class names is used more often in practice). However, whatever the choice, it should be consistent throughout the whole ontology. Some systems even require their users to declare in advance whether or not they are going to use singular or plural for concept names and do not allow them to stray from that choice.

Using the same form all the time also prevents a designer from making such modeling mistakes as creating a class Wines and then creating a class Wine as its subclass (see Section 4.1).

### 6.3 Prefix and suffix conventions
Some knowledge-base methodologies suggest using prefix and suffix conventions in the names to distinguish between classes and properties.  Two common practices are to add a has- or a suffix –of to property names.  Thus, our properties become has-maker and has-winery if we chose the has- convention. The properties become maker-of and winery-of if we chose the of- convention.  This approach allows anyone looking at a term to determine immediately if the term is a class or a property.  However, the term names become slightly longer.

### 6.4 Other naming considerations
Here are a few more things to consider when defining naming conventions:
- Do not add strings such as "class", "property", and so on to concept names.

It is always clear form the context whether the concept is a class or a property, for example. In addition is you use different naming conventions for classes and properties (say, capitalization and no capitalization respectively), the name itself would be indicative of what the concept is.
- It is usually a good idea to avoid abbreviations in concept names (that is, use Cabernet Sauvignon rather than Cab)
- Names of direct subclasses of a class should either all include or not include the name of the superclass. For example, if we are creating two subclasses of the Wine class to represent red and white wines, the two subclass names should be either Red Wine and White Wine or Red and White, but not Red Wine and White.

## 7. Other Resoues - Deleted

## 8. Conclusions
In this guide, we have described an ontology-development methodology for declarative frame-based systems. We listed the steps in the ontology-development process and addressed the complex issues of defining class hierarchies and properties of classes and instances. However, after following all the rules and suggestions, one of the most important things to remember is the following: there is no single correct ontology for any domain. Ontology design is a creative process and no two ontologies designed by different people would be the same. The potential applications of the ontology and the designer’s understanding and view of the domain will undoubtedly affect ontology design choices. “The proof is in the pudding”—we can assess the quality of our ontology only by using it in applications for which we designed it. 
