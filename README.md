# Document Generators
a simple set of LLM tools to generate documentation

> run all apps from the root folder

## Setup

1. Clone this repository
2. Install the required dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file in the project root and add your OpenAI API key:
```
   OPENAI_API_KEY=your_api_key_here
```



## Example Outline Format

```markdown
# Introduction
Brief overview of the topic

# Main Points
Key points to cover

# Conclusion
Summary and next steps
```




## Apps
### UIOpenDocGen
A Streamlit UI to allow editing of the content, prompt and output

#### Usage

1. Run the Streamlit application:
``` bash
 streamlit run UI/UIOpenDocGen.py    
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)
3. Enter your document outline in the left panel using markdown headers (#) to separate sections
4. Click "Generate Content" to create content for each section
5. View the generated content and improvement suggestions in the right panel


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
