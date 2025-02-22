# DocGen
a simple LLM tool to generate documentation

## apps

### OpenDocGen.py      

 A sample, that will read a markdown file, and split it into section sbased on the ``` ##``` tag, then for each section, the content is the prompt that will be passed to the LLM for generation

### DocGenReflext.py     
A sample agent based document generation. that has 3 steps, 
1. intital document generation
1. review the generated content and recomend improvements
1. update the document based on the review comments

### DocGenTeam.py
a sample that has set of agents that work together to produce a document

* **architect_agent** : the coordinating agent that controls the flow and passed work to other agents
* **reviewer_agent** : the agent reviews the content generated and suggests improvements
* **editor_agent** : the agent edits the document based on the comments from the reviewer
* **publisher_agent** : takes the final document and publishes this could include converting it to other formats such as DocX, PDF etc



## setup
create a folder 'GeneratedDoc' this is where the generated file will be placed

``` bash
pip install -r requirements.txt

```