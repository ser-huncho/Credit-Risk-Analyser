from execution_script import *
import streamlit as st
from streamlit_echarts import st_echarts
from time import sleep
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE SET UP
st.set_page_config(
     page_title = 'Credit Risk Analyzer',
     page_icon = 'icon.png',
     layout = 'wide',
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "### Credit Risk Analyzer. \n\n The purpose of this data-driven application is to automate the calculation of fees that make each new loan-customer binomial profitable by estimating the expected financial loss based on probability of default, loss given default, and exposure at default risk model predictions.\n&nbsp; \n  \n - Source code can be found [here](https://github.com/pedrocorma/credit-risk-scoring). \n - Further project details are available [here](https://pedrocorma.github.io/project/1riskscoring/)."
     })

# Page margins
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                .css-hxt7ib{
                    padding-top: 2.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# Sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 430px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 300px;
        margin-left: -300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

# SIDEBAR
with st.sidebar:
    st.image('img_sidebar.png')
    st.markdown('')

    col1, col2, col3, col4, col5 = st.columns([0.5,1,0.25,1,0.5])
    with col2:
        form_button = st.button('NEW LOAN APPLICATION')
    with col4:
        calculate_button = st.button('CALCULATE RISK')

    st.markdown('---')
    st.markdown("<h1 style='text-align: center; color: #f76497;'>SERVER-SIDE PARAMETERS</h1>", unsafe_allow_html=True)


    # Server-side features - Input
    col1,col2 = st.columns(2)
    with col1:
        scoring = st.select_slider('Profile scoring:',options=['A','B','C','D','E','F','G'],value='B')
        revolving_utilization = st.slider('% Revolving utilisation:', 0, 100, value=50)
        income_verification = st.radio('Income verification status:', ['Source verified','Verified','Not verified'], 0)
    with col2:
        dti = st.slider('Debt-to-income ratio:', 0, 100, value=18)
        p_credit_cards_exceeding_75p = st.slider('% Credit cards exceeding 75%:', 0, 100, value=37)
        n_derogations = st.radio('Previous derogations:', ['Yes','No'], 1)


# MAIN
# Title image
col1,col2,col3 = st.columns([0.8,1,0.5])
with col2:
    st.image('img_title.png')

placeholder = st.empty()

with placeholder.container():
    # st.markdown('')
    # Subtitle
    st.markdown("<h3 style='text-align: left; color: #f76497;'>LOAN APPLICATION FORM</h3>", unsafe_allow_html=True)
    st.markdown(' ')

    # Lead web form features - Input
    # Loan details
    st.markdown("<h5 style='text-align: left; color: #f76497;'>Loan details</h5>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2,0.25,1,0.25,2])
    with col1:
        loan_amount = st.number_input('Loan amount ($):',500,50000,12500,1,
                                      help="If the client wishes to apply for a loan amount above $50000 please refer him/her to the dedicated lending team.")
    with col3:
        term = st.radio('Term (months):',['36','60'],0)
    with col5:
        purpose = st.selectbox('Purpose:',
                               ['Debt consolidation','Credit card ','Home improvement','Major purchase','Medical',
                                'Small business','Car','Vacation','Moving','House','Wedding','Renewable energy','Educational','Other'],0)
    st.markdown('---')

    # Personal details
    st.markdown("<h5 style='text-align: left; color: #f76497;'>Personal  details</h5>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        employment_title = st.text_input('Employment title:', value='Teacher', max_chars=60, type="default")
    with col2:
        employment_length = st.select_slider('Employment length:',
                                             options=['< 1 year','1 year','2 years','3 years','4 years','5 years',
                                                      '6 years','7 years','8 years','9 years','10+ years'],value='3 years')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        annual_income = st.number_input('Annual income ($):',0,350000,65000,1,
                              help="If the client's annual income exceeds $350000 please refer him/her to the dedicated lending team.")
    with col2:
        home_ownership = st.selectbox('Home ownership status:',['Mortgage', 'Rent', 'Own', 'Any', 'Other', 'None'],0)
    with col3:
        n_credit_lines = st.number_input('Nº credit lines:',0,100,5,1)
    with col4:
        n_mortages = st.number_input('Nº mortages:',0,50,1,1)

    st.markdown('')

# Fixed data for simplicity:
## interest_rate
if scoring=='A':
    interest_rate = 7.08
elif scoring=='B':
    interest_rate = 10.68
elif scoring=='C':
    interest_rate = 14.15
elif scoring=='D':
    interest_rate = 18.13
elif scoring=='E':
    interest_rate = 21.78
elif scoring=='F':
    interest_rate = 25.44
elif scoring=='G':
    interest_rate = 28.13

## installment:
installment = round(loan_amount*(1+(interest_rate/100))/int(term),2)


df_loan = pd.DataFrame({'term':term + ' months',
                        'home_ownership':home_ownership.upper(),
                        'purpose':purpose.lower().replace(' ','_'),
                        'n_derogations':np.where(n_derogations=='Yes',1,0),
                        'employment_length':employment_length,
                        'scoring':scoring,
                        'annual_income':annual_income,
                        'dti':dti,
                        'installment':installment,
                        'interest_rate':interest_rate,
                        'loan_amount':loan_amount,
                        'n_credit_lines':n_credit_lines,
                        'n_mortages':n_mortages,
                        'revolving_utilization':revolving_utilization,
                        'employment_title':employment_title[0].upper() + employment_title[1:].lower(),
                        'income_verification':income_verification,
                        'p_credit_cards_exceeding_75p':p_credit_cards_exceeding_75p,
                        'client_id':1},
                        index=[0])


# CALCULATE RISK:
if calculate_button:
    df_el = run_models(df_loan)
    # st.dataframe(df_el)
    placeholder.empty()
    placeholder_results = st.empty()

    PD = float(df_el.probability_of_default)
    EAD = float(df_el.exposure_at_default)
    LGD = float(df_el.loss_given_default)
    EL = float(df_el.expected_loss)

    def formatter_custom(model,opt):
        if model=='PD':
            if opt==0:
                return('PD'+'\n'+str(round(PD*100))+'%')
            elif opt==1:
                return(str(round(PD*100))+'%')
        elif model=='EAD':
            if opt==0:
                return('EAD'+'\n'+str(round(EAD*100))+'%')
            elif opt==1:
                return(str(round(EAD*100))+'%')
        elif model=='LGD':
            if opt==0:
                return('LGD'+'\n'+str(round(LGD*100))+'%')
            elif opt==1:
                return(str(round(LGD*100))+'%')
        elif model=='EL':
            if opt==0:
                return('EL'+'\n'+str(round(EL,2))+' $')
            elif opt==1:
                return('Expected loss')

    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    col1,col2,col3,col4,col5 = st.columns([2.75,1,1,1,0.25])
    with col1:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'PD',
                              "value": EL,
                              "itemStyle": {"color": "#262730"}}],

                    "label": {"formatter": formatter_custom('EL',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#f76497',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": "#262730",
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'roundRect'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('EL',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=0)
    with col2:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'PD',
                              "value": PD,
                              "itemStyle": {"color": "#f76497"}}],

                    "label": {"formatter": formatter_custom('PD',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#fff',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": 'none',
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'container'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('PD',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=1)
    with col3:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'EAD',
                              "value": EAD,
                              "itemStyle": {"color": "#f76497"}}],

                    "label": {"formatter": formatter_custom('EAD',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#fff',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": 'none',
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'container'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('EAD',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=2)
    with col4:
        liquidfill_option = {
        "series": [{"type": "liquidFill",
                    "data": [{"name": 'LGD',
                              "value": LGD,
                              "itemStyle": {"color": "#f76497"}}],

                    "label": {"formatter": formatter_custom('LGD',0),
                              "fontSize": 40,
                              "color": '#f76497',
                              "insideColor": '#fff',
                              "show":"true"},


                    "backgroundStyle": {"borderWidth": 5,
                                        # "borderColor": 'red',
                                        "color": '#262730'},

                    "outline": {"borderDistance": 8,
                                "itemStyle": {"color": 'none',
                                              "borderColor": '#fff',
                                              "borderWidth": 2,
                                              "shadowBlur": 40,
                                              "shadowColor": '#f76497'}},

                    "amplitude": 5,
                    "shape": 'container'}],

        "tooltip": {"show": "true",
                    "formatter": formatter_custom('LGD',1)}
                    }

        st_echarts(liquidfill_option, width='100%', height='450%', key=3)


    col1,col2,col3,col4,col5,col6 = st.columns([0.22,2,0.18,0.9,0.9,1])
    with col2:
        st.markdown('Opening commission recommended to cover expected loss')
    with col4:
        st.markdown('Probability of default')
    with col5:
        st.markdown('Exposure at default')
    with col6:
        st.markdown('Loss given default')
        # "label": {"position": ['38%', '40%'],
        #           "formatter": "{b} : {c}%"
        #           "fontSize": 40,
        #           "color": '#D94854'}

        # }



    # for i in range(10,40):
    #     sleep(0.5)
    #     placeholder_results.empty()
    #
    #     options = {"yAxis": {"type": "category",
    #                         "data": ["PD", "EAD", "LGD"]},
    #
    #              "xAxis": {"type": "value", "max":100, "min":0},
    #
    #              "series": [{
    #
    #              "data": [i,i,i],
    #
    #              # "data": [float(df_el.probability_of_default),
    #              #                      float(df_el.exposure_at_default),
    #              #                      float(df_el.loss_given_default)],
    #                          "type": "bar",
    #                          "color": "#f76497",
    #                          "showBackground": "true",
    #                          "backgroundStyle": {"color": "rgba(180, 180, 180, 0.2)"}
    #                          }
    #                        ]
    #              }
    #
    #     with placeholder_results.container():
    #         st_echarts(options=options, width="100%", key=i, height='550%')




    # options = {"tooltip": {"trigger": 'axis',
    #                       "formatter": "{b} : {c}%",
    #                       "axisPointer": {"type": 'shadow'}},
    #           "grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},
    #
    #           "yAxis": [{"type": 'category',
    #                    "data": ["Probability of default", "Exposure at default", "Loss given default"],
    #                    "axisTick": {"alignWithLabel": "true"}}],
    #
    #           "xAxis": [{"type": 'value',"max":100,"min":0}],
    #
    #
    #           "series": [{"name": 'Prediction:',
    #                       "type": 'bar',
    #                       "color": "#f76497",
    #                       "barWidth": '60%',
    #                       "data": [round(float(df_el.probability_of_default*100),0),
    #                                round(float(df_el.exposure_at_default*100),0),
    #                                round(float(df_el.loss_given_default*100),0)]}]
    #           };
    #
    # st_echarts(options=options, width="100%", key=0, height='550%')

    # def formatter_function(val):
    #     if val == 0.875*100:
    #         return('A')
    #     elif val == 0.625*100:
    #         return('B')
    #     elif val == 0.375*100:
    #         return('C')
    #     elif val == 0.125*100:
    #         return('D')
    #     return('')
    #
    # with placeholder_results.container():
    #     chart_options = {
    #     "stateAnimation": {"duration":300,
    #                        "easing":"cubicOut"},
    #     "animation": "true",
    #     "animationThreshold":2000,
    #     "animationDuration": 1000,
    #     "animationEasing": "cubicInOut",
    #     "animationDelay": 500,
    #     "animationDurationUpdate": 1000,
    #     "animationEasingUpdate": "cubicInOut",
    #     "animationDelayUpdate": 500,
    #
    #     "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
    #     "series": [{"type": 'gauge',
    #                 "id": "ls",
    #                  "startAngle": 200,
    #                  "endAngle": -20,
    #                  "min": 0,
    #                  "max": 100,
    #                  "splitNumber": 10,
    #                 "animationThreshold": 2000,
    #                 "animationDuration": 1000,
    #                 "animationDurationUpdate": 1000,
    #                 "animationDelayUpdate": 500,
    #                 "animationEasing": 'cubicInOut',
    #
    #                  "axisLine": {"lineStyle": {"width": 5,
    #                                             "color": [[0.25, '#FF6E76'],
    #                                                       [0.5, '#FDDD60'],
    #                                                       [0.75, '#58D9F9'],
    #                                                       [1, '#7CFFB2']]}},
    #                  "pointer": {"icon": 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
    #                              "length": '15%',
    #                              "width": 20,
    #                              "offsetCenter": [0, '-65%'],
    #                              "itemStyle": {"color": 'auto'}},
    #                   "axisTick": {"length": 10,
    #                                "lineStyle": {"color": 'auto',
    #                                              "width": 1}},
    #                   "splitLine": {"length": 15,
    #                                 "lineStyle": {"color": 'auto',
    #                                               "width": 3}},
    #                   "axisLabel": {"color": '#464646',
    #                                 "fontSize": 25,
    #                                 "distance": -70,
    #                                 "formatter": formatter_function("{value}")},
    #                   "title": {"offsetCenter": [0, '-40%'],
    #                             "fontSize": 25},
    #                   "detail": {"valueAnimation": "true",
    #                              "fontSize": 80,
    #                              "offsetCenter": [0, '0%'],
    #                              "formatter": "{value}",
    #                              "color": 'auto'},
    #                   "data": [{"value": lead_score,
    #                             "name": 'Score'}]}],
    #                   "progress": {"show": "true", "width": 1,}
    #                             };
    #     st.markdown('---')
    #     col1,col2 = st.columns([1,0.8])
    #     if manage_lead=='Yes':
    #         with col1:
    #             st.markdown("<h4 style='text-align: center; color: #7CFFB2;'>It is cost-effective to manage this lead.</h4>", unsafe_allow_html=True)
    #         with col2:
    #             if lead_score >= 75:
    #                 st.markdown("<h4 style='text-align: center; color: #7CFFB2;'>Priority: Very high. </h4>", unsafe_allow_html=True)
    #             elif 50 <= lead_score < 75:
    #                 st.markdown("<h4 style='text-align: center; color: #58D9F9;'>Priority: High. </h4>", unsafe_allow_html=True)
    #             elif 25 <= lead_score < 50:
    #                 st.markdown("<h4 style='text-align: center; color: #FDDD60;'>Priority: Medium. </h4>", unsafe_allow_html=True)
    #             elif 25 > lead_score:
    #                 st.markdown("<h4 style='text-align: center; color: #FF6E76;'>Priority: Low. </h4>", unsafe_allow_html=True)
    #     elif manage_lead=='No':
    #         with col1:
    #             st.markdown("<h4 style='text-align: center; color: #FF6E76;'>It is not cost-effective to manage this lead.</h4>", unsafe_allow_html=True)
    #     st.markdown('---')
    #     results_plot = st_echarts(options=chart_options, width="100%", key=0, height='550%')



















##
