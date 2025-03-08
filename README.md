# DocGen
a simple LLM tool to generate documentation

> run all apps from the root folder

## Apps
### UIOpenDocGen
A Streamlit UI to allow editing of the content, prompt and output

``` bash
 streamlit run UI/UIOpenDocGen.py    
```
### OpenDocGen.py

 A sample, that will read a markdown file, and split it into section based on the ``` ## ``` tag, then for each section, the content is the prompt that will be passed to the LLM for generation
 
``` bash
 python OpenDocGen/OpenDocGen.py   
 ```

### DocGenReflect.py

A sample agent based document generation. that has 3 steps,

1. initial document generation
1. review the generated content and recommend improvements
1. update the document based on the review comments


``` bash
  python DocGenReflect/DocGenReflect.py             
 ```
 
### DocGenTeam.py

a sample that has set of agents that work together to produce a document

``` bash
python DocGenTeam/DocGenTeam.py     
```

| **Team Member**        | **Role**            |
|------------------------|---------------------|
| **coordinator_agent**  | Manages the workflow between agents.      |
| **architect_agent**    | Creates the initial architectural document.      |
| **reviewer_agent**     | Reviews the document for errors, best practices, and security considerations.      |
|  **editor_agent**      | Edits the document based on the review feedback.      |
|  **publisher_agent**   | prepares and formats the document for publishing.      |

## Setup

create a folder 'GeneratedDoc' this is where the generated file will be placed

``` bash
pip install -r requirements.txt

```
