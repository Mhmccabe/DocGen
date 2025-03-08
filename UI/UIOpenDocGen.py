import streamlit as st
from DocGenTools import LangChainHandler, extract_sections, generate_markdown_download

def main():
    st.set_page_config(layout="wide")
    
    # Initialize LangChain handler
    if 'langchain_handler' not in st.session_state:
        st.session_state.langchain_handler = LangChainHandler()
    
    # Add the download button to the toolbar using session state to ensure it's always at the top
    if 'generated_content' in st.session_state:
        # Create markdown content from the edited sections
        sections = [
            {
                'title': section['title'],
                'content': st.session_state.edited_content.get(i, section['content'])
            }
            for i, section in enumerate(st.session_state.generated_content)
        ]
        markdown_content = generate_markdown_download(sections)
        
        # Position the download button in the top-right corner
        col1, col2 = st.columns([6, 1])
        with col2:
            st.download_button(
                label="Download MD",
                data=markdown_content,
                file_name="generated_document.md",
                mime="text/markdown",
                help="Download the generated content as a markdown file"
            )

    # Initialize session state for edit mode and content
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {}
    if 'edited_content' not in st.session_state:
        st.session_state.edited_content = {}

    # Create two columns for split screen
    left_col, right_col = st.columns(2)

    with left_col:
        st.header("Content Context")
        context_input = st.text_area(
            "Enter context or guidelines for the AI to consider while generating content:",
            height=150,
            placeholder="""Example:
- Write in a professional but accessible tone
- Use concrete examples to illustrate points
- Focus on practical applications
- Include relevant statistics when possible
- Maintain consistency with company style guide""",
            help="This context will guide the AI in generating and improving content. It acts like a system prompt or set of guidelines."
        )

        st.header("Document Outline")
        markdown_input = st.text_area(
            "Enter your document outline in markdown format (use # for headers):",
            height=500,
            placeholder="""# Introduction
Brief overview of the topic

# Main Points
Key points to cover

# Conclusion
Summary and next steps"""
        )

        if st.button("Generate Content"):
            if not markdown_input:
                st.warning("Please enter a document outline first.")
            else:
                with st.spinner("Generating content..."):
                    sections = extract_sections(markdown_input)
                    generated_content = []
                    
                    for section in sections:
                        if section["is_empty"]:
                            # For empty sections, keep the original content without generation
                            generated_content.append({
                                "title": section["title"],
                                "content": section["content"].strip(),
                                "improvements": [],
                                "is_empty": True
                            })
                        else:
                            # Generate content only for non-empty sections
                            content = st.session_state.langchain_handler.generate_content(section, context_input)
                            improvements = st.session_state.langchain_handler.improve_content(content, context_input)
                            
                            generated_content.append({
                                "title": section["title"],
                                "content": content,
                                "improvements": improvements.split('\n'),
                                "is_empty": False
                            })
                    
                    st.session_state.generated_content = generated_content
                    # Initialize edit mode and edited content for new sections
                    for i, section in enumerate(generated_content):
                        if i not in st.session_state.edit_mode:
                            st.session_state.edit_mode[i] = False
                        if i not in st.session_state.edited_content:
                            st.session_state.edited_content[i] = section['content']

    with right_col:
        st.header("Generated Content")
        if 'generated_content' in st.session_state:
            for i, section in enumerate(st.session_state.generated_content):
                st.markdown(f"## {section['title']}")
                
                # Add edit mode toggle with checkbox
                st.session_state.edit_mode[i] = st.checkbox(
                    "Edit Mode",
                    value=st.session_state.edit_mode.get(i, False),
                    key=f"edit_toggle_{i}",
                    help="Toggle between edit and read mode"
                )
                
                # Edit mode or display mode based on state
                if st.session_state.edit_mode[i]:
                    # Edit mode
                    edited_text = st.text_area(
                        "Edit content:",
                        value=st.session_state.edited_content.get(i, section['content']),
                        height=300,
                        key=f"editor_{i}"
                    )
                    st.session_state.edited_content[i] = edited_text
                else:
                    # Display mode
                    st.markdown(st.session_state.edited_content.get(i, section['content']))
                
                # Only show improvements for non-empty sections
                if not section.get('is_empty', False) and section['improvements']:
                    with st.expander("Suggested Improvements"):
                        for improvement in section['improvements']:
                            if improvement.strip():
                                st.markdown(f"- {improvement}")
                st.markdown("---")

if __name__ == "__main__":
    main() 