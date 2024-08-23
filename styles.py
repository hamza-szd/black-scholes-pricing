import streamlit as st

def apply_css():
    # CSS Styling for the Streamlit page
    st.markdown("""
        <style>
        .metric-container {
            display: flex; 
            justify-content: center;
            align-items: center;
            padding: 8px; 
            width: auto; 
            margin: 0 auto; 
        }

        .call { /* For the custom call pricing class */
            background-color: #90ee90; 
            color: black; 
            margin-right: 10px;
            border-radius: 10px;
        }

        .put { /* For the custom put pricing class */
            background-color: #ffcccb;
            color: black; 
            border-radius: 10px; 
        }

        .value {
            font-size: 1.5rem; 
            font-weight: bold;
            margin: 0;
        }

        .label { /* For the label class */
            font-size: 1rem;
            margin-bottom: 4px;
            margin-right: 5px; /* Space between label and tooltip */
            display: inline-flex;
            align-items: center;
        }

        .tooltip {
            position: relative;
            display: inline-flex;
            align-items: center;
        }

        .tooltip .tooltip-text {
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 125%; /* Position above the icon */
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.5s;
        }

        .tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }

        .question-icon {
            font-weight: bold;
            color: #4e739c;
            font-size: 16px;
            border: 1px solid #007bff;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            cursor: pointer;
            float: right;
        } 

        .fields {
                margin-bottom: -20px;
        }   
    </style>""", unsafe_allow_html=True)


def help_icon(description):
    return f"""
    <div class="tooltip">
        <span class="question-icon">?</span>
        <span class="tooltip-text">{description}</span>
    </div>
    """

