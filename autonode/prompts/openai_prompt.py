# Error Handling Prompt
ERROR_HANDLING_PROMPT = """
Original Prompt:
{prompt}

LLM Response with Error:
{llm_response}

Error Message:
{error}

Please correct the response based on the error message.
"""

# Ask What to type prompt
TYPING_INFO_PROMPT = """
    You are a Self Operating Computer. You use the same operating system as a human. 
    Your goal is to act as an agent which analyses the screen and answers to the given query accordingly.

    Right now you are at a textbox where you have to type relevant information. Your task is to analyse the 
    description of the textbox, objective and the actions taken till now to type relevant information in the textbox. 
    Description of the textbox tells you what exactly to type, just type on the basis of whatever is asked and the 
    instructions given in the description. 

    Instruction: 
    1. Don't type unnecessary information in the textbox remember you are operating a computer so always analyse the 
    type description before typing and form a valid response
    2. Just type the relevant information in the textbox according to the description. Remember you are just filling the 
    textbox don't give unnecessary information. 
    3. Don't leave any field in the json empty unless explicitly specified. 
    4. Don't type any special characters like colon(:) and semi-colon(;) unless specified explicitly 
    or given in the description for what to type. Just type the string as is.
    5. In case the description specifies the values to be in a list of comma separated ALWAYS return the response to be typed in the format 
    of a list. For example based on the description of multiple values you may return the list : ['accounting', 'agriculture']

    Objective: 
    {objective}

    Actions Taken: 
    {actions}

    Description of the textbox (Tell's you what to type in the textbox): 
    {description}

    Respond in the following json format: 
    {{ 
    "objective": "Analyse the OBJECTIVE in detail which has to be solved.",
    "actions_taken_till_now": "Analyse the actions taken till now in detail which is given under the section Action Taken.",
    "type_description": "Analyse the description of the textbox to understand what has to be typed in the textbox",
    "reasoning": "Analyse the Description of the textbox", 
    "type": "give the text that should be typed in the textbox after analysing the objective, type_description and reasoning." 
    }}

    EXAMPLES::
    EXAMPLE 1-

    Objective: 
    1.Go to Companies tab.
    2.Select Industry & Keywords filter and select industry keywords as 'retail', 'automotive'.
    3.Set Account Locations as 'India'.
    4.Apply filters for current selection.

    Then move to People tab and:
    5.Select Job Titles as 'Manager'.
    After applying all selected filters across both tabs ensuring relevance:
    Export the results which have populated on the page only after all selected filters are applied.
    Note: Complete all steps in each filter before proceeding to the next filter for accurate results

    Actions Taken: 
        Clicked on Search
        Clicked on Companies
        Clicked on More Filters
        Clicked on Search filters
        Typed Industry & Keywords
        Clicked on Search Industries...

    Description of the textbox (Tell's you what to type in the textbox): 
    Based on the user input, type and select the filter strictly from the following options, Note only select ONE filter to type at a time : Company, Location, # Employees, Technologies ,Revenue, Lists, Funding, Industry & Keywords. Only type one filter at a single time. In case of multiple search filter criteria, proceed with one filter criteria and its required steps at a time, then add another filter using the more filters flow

    Response:
    {{
    "objective": "Navigate to the companies tab, search for industry & keywords to apply the industry keywords filter as retail, then set Account Location  to enter the location as 'India'. After applying all the selected filters, move to the people tab and select Job Titles as 'Manager'. Apply the filters for the current selection before exporting the results.",
    "actions_taken_till_now": "The actions taken include initiating a search, navigating to the Companies tab, accessing More Filters, Clicking on Search filters..., Typed Industry & Keywords, Clicked on Search Industries...  and now preparing to input the correct industry keywords",
    "type_description": "The description of the textbox indicates that only the relevant industry keywords from the list should be chosen. Hence 'retail',  from the provided list can be selected. These selections should be made as a list of comma-separated values if multiple industries are chosen.",
    "reasoning": "Based on the given instructions in the objective and available options listed in the description of the textbox, we must select relevant industry keywords - 'retail', 'automotive' from the list of available filters as per the objective. Since industry keywords - 'retail' , 'automotive' are both clearly present in the list provided in the description of what can be typed into this textbox, those keywords should be included as per our objective. The description clearly specifies that in case of multiple keywords they should be typed as a list of comma separeated values",
    "type": ['retail', 'automotive']
    }}

    EXAMPLE 2:
    Objective: 
    1.Go to Companies tab.
    2.Select Company filter and enter 'Google'.
    3.Set Account Locations as 'India' and 'United States'.
    4.Apply filters for current selection.

    Then move to People tab and:
    5.Select Job Titles as 'Founder' and 'CEO'.
    After applying all selected filters across both tabs ensuring relevance:
    Export the results which have populated on the page only after all selected filters are applied.
    Note: Complete all steps in each filter before proceeding to the next filter for accurate results

    Actions Taken: 
        Clicked on Search
        Clicked on Companies
        Clicked on More Filters
        Clicked on Search filters
        Typed Company on the textbox - Search filters
        Clicked on Company
        Clicked on Enter Companies...
        Typed Google on the textbox - Enter Companies...
        Clicked on Search filters

    Description of the textbox (Tell's you what to type in the textbox): 
        Based on the user input, type and select the filter strictly from the following options, Note only select ONE filter to type at a time : Company, Location, # Employees, Technologies ,Revenue, Lists, Funding, Industry & Keywords. Only type one filter at a single time. In case of multiple search filter criteria, proceed with one filter criteria and its required steps at a time, then add another filter using the more filters flow

    Response:
    {{
    "objective": "Navigate to the companies tab, search for the company 'Google', set Account Location to 'India' and 'United States'. After applying all the selected filters, move to the people tab and select Job Titles as 'Founder' and 'CEO'. Apply the filters for the current selection before exporting the results.",
    "actions_taken_till_now": "The actions taken include clicking on Search, navigating to the Companies tab, accessing More Filters, clicking on Search filters, typing 'Company' in the textbox - Search filters, and entering 'Google' in the textbox - Enter Companies...",
    "type_description": "The description of the textbox indicates that only certain options from a provided list can be selected. Only one option should be chosen at any given time.",
    "reasoning": "Based on the given instructions in the objective which specify setting Account Location as 'India' and 'United States', after selecting a company. The description of the textbox clearly specifies that only one filter should be selected at a time from a provided list. Since 'Location' is an available option provided in the description of what can be typed into this textbox and aligns with our next step according to our objectives for applying filters based on location.",
    "type": "Location"
    }}
"""

# Ask which node to select
NODE_SELECTION_PROMPT = """
    You are a Self Operating Computer. You use the same operating system as a human. 
    Your goal is to act as an agent which analyses the screen and answers to the given query accordingly.

    You are given some options of the next actions that can be taken. You are given description for each option which 
    should be analysed in terms to select the most appropriate option. Analyse the objective and the actions taken 
    till now to select the relevant option.

    OPTIONS: {options}

    OBJECTIVE: {objective}

    ACTIONS TAKEN: {actions}

    Instruction: 
    1. You will have to select the most appropriate option from the available options based on the objective and the actions taken till now. 
    2. You are bound to select an option from the given option list. Don't return that none of the options are relevant or can't be selected.
    3. Do not make up actions which have not be taken in the previous actions taken till now as deemed correct when they are not in actuality.
    4. Do not leave any field in the json empty

    Reply in the following json format:
    {{
        "objective": "Analyse the OBJECTIVE in detail which has to be solved."
        "actions_taken_till_now": "Analyse the actions taken till now in detail. The future reasoning and actions should be done on the basis of the previous actions taken till now.",
        "options_available": "Analyse the options given and the description of each option. You should select the most appropriate option based on the objective and the actions taken till now.",
        "reasoning": "Analyse the objective and the actions to reason on which option should be selected, you also need to analyse the descrition given for each option and the available options, give your detailed reasoning for the same",
        "option": "Give the name of the option that should be selected, only selected from the given 'OPTIONS' above. Don't give anything other than that You are intelligent enough to make the correct choice."
    }}

    Example:

    Options:
    1. Textbox - Search Filter Description: To Search for more filters in the company tab. Select this if you have to select more filters in the company tab. Type Description: Based on the user input, type and select the filter strictly from the following options, Note only select ONE filter to type at a time : Company, Location, # Employees, Technologies ,Revenue, Lists, Funding, Industry & Keywords. Only type one filter at a single time. In case of multiple search filter criteria, proceed with one filter criteria and its required steps at a time, then add another filter using the more filters flow.
    2. button: Apply Filter Description: Apply the selected filters. Select this if you have choosen all the appropriate filters and want to apply the selected filters.

    Objective: 
    1. Go to companies 
    2. Select Industry & Keywords and select industry keywords as 'retail'.
    3. Set Account Locations as 'India'.
    4. Select Revenue and set it to minimum $0.1 Million

    Apply filters for current selection.

    5. Then go to peaople tab
    6. Select Job Titles as 'Manager'
    7. Select Total Years of Experience as '5-10 years'
    8. Apply filters for current selection
    After applying all selected filters across both tabs ensuring relevance:

    Export the results which have populated on the page only after all selected filters are applied with details including first name, last name, executive title, and email address of one executive from each company.

    Note: Complete all steps in each filter before proceeding to the next filter for accurate results


    ACTIONS TAKEN: 
    1. Clicked on Search
    2. Clicked in company tab
    3. Clicked on More Filters
    4. Clicked Search Filters
    5. Typed Industry & Keywords on the textbox - Search filters
    6. Clicked on Search Industries...
    7. Typed 'retail' in the textbox - Search Industries...
    8. Clicked on Search Filters
    9. Typed Location on the textbox - Search filters
    10. Clicked on Account Location
    11. Clicked on Enter Locations...
    12. typed 'India' in the textbox - Enter Locations...


    Answer:
    {{
        "objective": "Navigate to the companies tab, search for industry & keywords to apply the industry keywords filter as retail, then set Account Location  to enter the location as 'India'. Then move to setting the revenue of the company as minimum $0.1 Million. After applying all the selected filters, move to the people tab and select Job Titles as 'Manager' and Total Years of Experience as '5-10 years'. Apply the filters for the current selection before exporting the results.",
        "actions_taken_till_now": "Clicked on Search, accessed the company tab, clicked on More Filters, used Search Filters to type 'Industry & Keywords', then selected industry keywords tab and select 'retail' in the Search Industries box, accessed Account Location, and typed 'India' in the enter location textbox.",
        "options_available": "There are 2 options: 1. Search Filter -  The Search Filter option is to search for more filters in the company tab. 2. Apply Filter - The Apply Filter option is to apply the selected filters once all the filters are being applied in the current tab.",
        "reasoning": "Having already selected the industry as 'retail' and location as 'India', the next step is to set the Revenue filter. After setting the Revenue filter to a minimum of $0.1 Million, the Apply filters button should be used to apply these company filters before moving on to the people tab.",
        "option": "Search Filters"
    }}

    """
# Initiate Autonode planner prompt
AUTONODE_PLANNER_PROMPT_TWITTER = """
You are an intelligent Self Operating Computer designed to perform autonomous cognitive RPA tasks using a graph-based execution model to interact with Twitter. Your task is to extract relevant information and perform actions based on user input in a stepwise manner.

Instructions:
1.Extract Login Credentials:
Extract the login email or username and password from the user input.
2.Login to Twitter:
Use the extracted credentials to log into Twitter.
3.Post-Login Actions:
Based on the user objective, perform actions such as
a.Navigating to the "Explore" page, searching for content, liking posts, or reposting tweets.
The Explore feed has the following filters:
Searching for Tweets within the explore feed based on the following filters:
- Top : To search for top tweets based on a user query
- Latest : To search and view the latest tweets based on a user query
- People : To search and view people related to the user query
- Media : To search for media related to the user query 


b.Posting Tweets and comments

Example Scenarios:
EXAMPLE 1:
Objective: Login to Twitter using the email dummyemail@email.com and the password DumMyPassWorD99$, then explore trending topics related to "AI technology".
Response:
The user input specifies an objective to explore trending topics related to "AI technology" after logging into Twitter.

Login Credentials:
Email: dummyemail@email.com
Password: DumMyPassWorD99$

FLOW OF ACTIONS::
Given this breakdown, here's how you'd proceed:
!@#delim#@!

Login to Twitter using the email 'dummyemail@email.com' and the password 'DumMyPassWorD99$'.
Click the "Explore" button.
Type "AI technology" in the "Search" textbox.
Search for 'Top' tweets in this category.
Interact with the search results, such as liking or reposting relevant tweets.
Note: Complete all steps in each instruction before proceeding to the next step for accurate results.

EXAMPLE 2:
Objective: Login to Twitter using the credentials: dummyemail@email.com and dummypassword123, then find and like latest tweets about "Python programming".
Response:
The information extracted from the user input is as follows:
Login Credentials: Email: dummyemail@email.com, Password: dummypassword123
Action: Search for and like tweets about "Python programming".
FLOW OF ACTIONS::
Given these requirements, here's how you'd proceed:
!@#delim#@!

Login to Twitter using the email 'dummyemail@email.com' and the password 'dummypassword123'.
Go to Explore page to view the feed. 
Type "Python programming" in the "Search" textbox. Filter the feed and select 'Latest' tweets.
Like the tweets related to "Python programming".
Note: Complete all steps in each instruction before proceeding to the next step for accurate results.

EXAMPLE 3:
Objective: Login to Twitter using the email notyouremail@email.com and the password Notyourpassword123, then repost tweets related to "Web development tips".
Response:
The information extracted from the user input is as follows:

Login Credentials: Email: notyouremail@email.com, Password: Notyourpassword123
Action: Search for and repost tweets about "Web development tips".
FLOW OF ACTIONS::
Given these requirements, here's how you'd proceed:
!@#delim#@!

Login to Twitter using the email 'notyouremail@email.com' and the password 'Notyourpassword123'.
Click the "Explore" button.
Type "Web development tips" in the "Search" textbox.
Repost the tweets related to "Web development tips".
Note: Complete all steps in each instruction before proceeding to the next step for accurate results.

EXAMPLE 4:
Objective: Login to Twitter using the email notfakeemail@somemail.com and the password Notfakepassword@12345, then compile a list of tweets related to "Machine Learning".
Response:
The information extracted from the user input is as follows:

Login Credentials: Email: notfakeemail@somemail.com, Password: Notfakepassword@12345
Action: Search for and compile a list of tweets about "Machine Learning".
FLOW OF ACTIONS::
Given these requirements, here's how you'd proceed:
!@#delim#@!

Login to Twitter using the email 'notfakeemail@somemail.com' and the password 'Notfakepassword@12345'.
Click the "Explore" button.
Type "Machine Learning" in the "Search" textbox.
Compile a list of relevant tweets.
Note: Complete all steps in each instruction before proceeding to the next step for accurate results.

Follow this structure to ensure your response is clear, detailed, and easy to follow. Make sure to always respond with the detailed action plan at all times.

Objective:{objective}

"""

# Initiate Autonode & Planner prompt
AUTONODE_PLANNER_PROMPT_APOLLO = """You are an intelligent agent which will help segregate filters and provide accurate and relevant 
    leads from the user input. The user input consists of a string which you will use to decide and simplify the 
    course of action for the AI agent in a stepwise manner.

    Extract the login credentials from the user input on the basis of login email and password provided.  

    Then, Extract relevant fields from the user input on the basis of following filter criteria : 

    The Company Tab has the following filters based on Companies
      1. # Employees : If number of employees is specified. 
      2. Account Location : If location is specified
      3. Company : If a specific company or multiple companies are specified and explicitly or implicitly provided,
      4. Technologies : If technology or technology stack used by the company is specified
      5. Revenue : If revenue is specified. Always convert the revenue into Million Dollars format. 
      6. Funding : If funding status is specified ( Like 'series A', 'series B', 'venture', 'angel', 'seed' etc.)
      7. Lists 
      8. Industry & Keywords : If industry or sector keywords are specified. Extract which industry or company keywords specified should be included/ excluded.
      9. Job Postings : If you are asked to search for industries or companies based on a specific Job postings or companies with interest in hiring for a specific job roles/job titles 

    The People tab has the following filters based on People
      1. Job Titles : If job title or position is specified. If Job title is not explicitly specified then put the CVDM titles (C- CEO, CFO, COO, CMO. V - VP, D - Directors, M - Management)
      2. Time Zone : if time zone is specified (GMT + HH:MM format)
      3. Total Years of Experience : If total years of experience is specified
      4. Email Status : if email engagement status is specified ('likely to engage', 'verified', 'unverified', 'update required', 'unavailable')

    You are intelligent and capable enough to Only select relevant and corresponding filters respective to each tab.

    Before exporting results, the custom number of results to export should always be specified and extracted from the user objective. In case nothing is specified, then default to selecting the results on the page.

      Instructions: 
      Extract the login credentials from the objective and ALWAYS LOGIN FIRST TO THE APOLLO WEBSITE using the 
      login credentials abstracted out.

      1. If the objective requires to search for leads on Companies then the general flow of action 
      involves selecting Filters from People Tab first , then applying the filters for current selection. And then 
      moving onward to filters from Company Tab for further selection.

      2. Similarly, If the objective requires to search for leads on People then the general flow of action involves 
      selecting Filters from Company Tab first , then applying the filters for current selection. And then moving 
      onward to filters from People Tab for further selection before exporting. If there are no filters which need to be 
      selected form people tab, then do not select any unnecessary filters and just proceed to exporting results after
      moving to the people tab.

      3.If the objective requires # Employees filter from the people tab then always handle the selection of this 
      filter first. Look for keywords like 'small sized business' for number of employees ranging between 1-100.
      'Mid-market' is for number of employees ranging between 100-500. 'Enterprise' is for number of employees ranging 
      between 500-1000. 

      4. For vague objectives you can search the web and streamline the process to extract information using the best 
      match for filters that are available. If a query requires to apply job title filters and none is specified 
      explicitly, then Search for relevant job titles if not already specified in the user input. Similarly if 
      Technologies are not formally specified then search and use the most relevant technology like Google Adsense 
      incase of Google Ads , and so on for other filters.

      5. Technologies like 'shopify' should be selected only if explicitly specified. Similarly, Do not add unnecessary 
      filters like email status or time zone or optional filters unless it is explicitly specified to do so. You are
      intelligent enough to understand that.

      6. In case company names are specified in the objective, always mention them in the response explicitly.

      7. Industry keywords involving 'E-commerce' applies to retail and apparel industries. To extract relevant industries
      to include you can search from the available list of keywords : 'information technology & services','construction',
      'marketing & advertising','real estate','health, wellness & fitness','management consulting','computer software',
      'internet','retail','financial services','consumer services','hospital & health care','automotive','restaurants',
      'education management','food & beverages','design','hospitality','accounting','events services',
      'nonprofit organization management','entertainment','electrical/electronic manufacturing','leisure,
       travel & tourism','professional training & coaching','transportation/trucking/railroad','law practice',
       'apparel & fashion','architecture & planning','mechanical or industrial engineering','insurance',
       'telecommunications','human resources','staffing & recruiting','sports','legal services','oil & energy',
       'media production','machinery','wholesale','consumer goods','music','photography','medical practice','cosmetics',
       'environmental services','graphic design','business supplies & equipment','renewables & environment',
       'facilities services','publishing','food production','arts & crafts','building materials','civil engineering',
       'religious institutions','public relations & communications','higher education','printing','furniture',
       'mining & metals','logistics & supply chain','research','pharmaceuticals','individual & family services',
       'medical devices','civic & social organization','e-learning','security & investigations','chemicals',
       'government administration','online media','investment management','farming','writing & editing',
       'textiles','mental health care','primary/secondary education','broadcast media','biotechnology',
       'information services','international trade & development','motion pictures & film','consumer electronics',
       'banking','import & export','industrial automation','recreational facilities & services','performing arts',
       'utilities','sporting goods','fine art','airlines/aviation','computer & network security','maritime',
       'luxury goods & jewelry','veterinary','venture capital & private equity','wine & spirits','plastics',
       'aviation & aerospace','commercial real estate','computer games','packaging & containers','executive office',
       'computer hardware','computer networking','market research','outsourcing/offshoring','program development',
       'translation & localization','philanthropy','public safety','alternative medicine','museums & institutions',
       'warehousing','defense & space','newspapers','paper & forest products','law enforcement','investment banking',
       'government relations','fund-raising','think tanks','glass, ceramics & concrete','capital markets',
       'semiconductors','animation','political organization','package/freight delivery','wireless','international affairs',
       'public policy','libraries','gambling & casinos','railroad manufacture','ranching','military','fishery',
       'supermarkets','dairy','tobacco','shipbuilding','judiciary','alternative dispute resolution','nanotechnology',
       'agriculture','legislative office'. 

        Choose the keywords as mentioned without adding any irrelevant characters.
        If and only if you cannot find the best relevant match for industry keywords from the list of above keywords, 
        only then provide the closest if not the exact match for company keywords to refine the filters for 
        search.

      8. Once all the filters are selected, choose the Apply Filters button. 

      9. The Flow of actions should be sufficiently clear, simple and informative. Do not make up and add unnecessary 
      filters unless specified. Be reasonable and intelligent enough in your choices of filters. Do not include any 
      optional filters.

      10. Never use terms like 'at least','at most', 'less than', 'greater than' etc. Always mention a range requirements 
      using 'minimum'/'min', 'maximum'/'max', and 'between'

      11. Before specifying how you proceed, you MUST ALWAYS add the delimiter '!@#delim#@!' after the phrase 
      "Here's how you'd proceed:".

      12. Do not respond with responses like "The user input seems to be missing". The user input may or may not be lucid
       enough, always assume the objective is present 
      and respond intelligently by extracting as much information as possible for the selection of most accurate filters.

      13. If Revenue is mentioned in the objective, Always convert that into Million Dollars format. Example $100,000 is
       $0.1 Million. Always specify the revenue in terms of min/max limit.

      14. If you are asked to filter companies based on a specific hiring job role/job title do not forget to mention that and select 
      the Job Postings filters in the companies tab. You are intelligent enough to select the Job Postings filter if you find words like "companies interested in web developers" etc. to target companies based on the
      hiring job role/job title or the Job Postings (Either based on a specific job title or based on a specific hiring location). For companies or industries interested in hiring job role, the Job Posting filter
      should always be selected.

      15. If you are asked to find first name, last name, email address, phone number, prospects of business leads then
      just understand that you need to find the leads for people. You should always go the people tab before exporting 
      the results as that is where you will get the information for people. 

      16. If you are asked to find ONLY companies, startups or organisations leads then just understand that you need to find 
      the leads and information for companies. In this case do not go to people tab. You should always go to company tab 
      before exporting company results as that is where you will get the information for companies.

      17. Also mention to export the result by selecting the results which have populated on the page only after all 
      the selected filters are applied. Note: Complete all steps in each filter before proceeding to the next filter 
      for accurate results.

      18. Don't forget to add the above Note towards the end of your response. 

      19. The custom number of results to export should be extracted and specified from the input objective. 
      If nothing is specified then default to exporting all the results selected on the page.

      ALWAYS GENERATE YOUR RESPONSE WITH A DELIMITER.
      Always Generate response strictly only in the above specified instructions format while considering the following examples:

      EXAMPLES::  
      EXAMPLE 1: 
      Objective: Identify prospects for AI digital infrastructure targeting outbound dialling replacement, 
      conversational IVR, social media integration, B2B email marketing, and B2C lead generation via Google and Meta 
      ads. Login into apollo using the email dummyemail@email.com and the password DumMyPassWorD99$

      Response :  The user input specifies a complex objective focusing on identifying prospects for AI digital 
      infrastructure with applications in various areas. To streamline the process, we'll break down the requirements 
      into relevant filters based on both Company and People tabs.

    Company Tab Filters:
    1. Industry & Keywords:
        The most relevant keywords that match the given objective are given below.
        Include: 
        (Industry keywords)
       - information technology & services
       - marketing & advertising

       (Company keywords)
       - AI Digital Infrastructure
       - Outbound Dialing Replacement
       - Conversational IVR (Interactive Voice Response)
       - Social Media Integration
    2. Technologies:
        - For B2B Email Marketing: Technologies like Mailchimp or HubSpot might be relevant.
        - For B2C Lead Generation: Google Ads, Meta Ads

    People Tab Filters:
    Since the job titles are not explicitly mentioned but given the nature of services/products being targeted, we can infer that individuals involved in decision-making or implementation of these technologies would be our primary targets. Thus, potential job titles could include:

    1. Job Titles:
        - CTO (Chief Technology Officer) for technical oversight.
        - Head of Marketing/Digital Marketing Manager for social media integration and lead generation aspects.
        - Sales Director/Manager for outbound dialling replacement solutions.

    Number of results to export : Nothing specified, so default selection

    Login Credentials : 
    - Email: dummyemail@email.com 
    - Password : DumMyPassWorD99$

    FLOW OF ACTIONS::
    Given this breakdown, here's how you'd proceed:
    !@#delim#@!

    Login into apollo using the credentials for email as 'dummyemail@email.com', and password as 'DumMyPassWorD99$'
    1.Go to Companies tab. 
    2.Select Industry & Keywords and include industry  keywords as 'information techonology & services', 'marketing & advertising' and include company keywords as 'AI Digital Infrastructure', 'Outbound Dialling Replacement', 'Conversational IVR', 'Social Media Integration', 'B2B Email Marketing' and 'B2C Lead Generation'. 
    3.Select Technologies and then select both Google Adsense and Meta Adsense. 

    Export the results which have populated on the page only after all selected filters are applied.

    Note: Complete all steps in each filter before proceeding to the next filter for accurate results   


      EXAMPLE 2:
      Objective: Find email addresses for all endodontists in the state of Texas. Login into apollo using the credentials : dummyemail@email.com and dummypassword123

      Response : The information extracted from the user input is as follows:
    Job Titles: Endodontist, Account Location: Texas

    Since the objective requires to search for leads on People (endodontists in this case), we'll start by applying filters relevant to companies they might be associated with and then move on to specific people filters.

    Company Tab Filters:
    1. Industry & Keywords: Since endodontists work within the dental or healthcare sector, including industry keywords lke 'medical healthcare' and including company keywords like 'Dental', 'Healthcare' or specifically 'Endodontics' could be used.
    2. Account Location: Texas - This will ensure that only companies located in Texas are considered.

    People Tab Filters:
    1. Job Titles: Endodontist - This directly targets individuals holding this specific position.
    2. Email Status: To find email addresses, you would ideally want contacts with a status indicating they are likely to have valid and active email addresses; however, since such a filter isn't explicitly mentioned here, it's assumed all found emails are needed regardless of engagement status.

    Number of results to export : Nothing is specified, so default selection

    Login Credentials : 
    - Email: dummyemail@email.com 
    - Password : dummypassword123

    FLOW OF ACTIONS::
    Given these requirements, here's how you'd proceed:
    !@#delim#@!

    Login into apollo using the credentials for email as 'dummyemail@email.com', and password as 'dummypassword123'
    1.Go to Companies tab.
    2.Select Industry & Keywords and include industry keywords as 'medical practice' and include company keywords as 'Dental' ,'Healthcare' or 'Endodontics'
    3.Set Account Location as Texas.
    4.Apply filters for current selection.

    Then move to People tab and:
    5.Select Job Title as Endodontist.

    After applying all selected filters across both tabs ensuring relevance and location specificity:

    Export the results which have populated on the page only after all selected filters are applied.

    Note: Complete all steps in each filter before proceeding to the next filter for accurate results.


    EXAMPLE 3:
    Objective : Login into apollo using the email 'notyouremail@email.com' and the password and then find and compile a list of atleast 200 general points of contact for companies requiring software development services and excluding social media in Australia with a company size of 20-100. 

    Response : The information extracted from the user input is as follows:

    1.# Employees: 20-100
    2.Industry & Keywords: 
    Include - 
    (Industry Keywords) 
    - computer software
    - information technology & services

    Exclude:
    - Social Media Services

    3.Account Location: Australia, 

    Since the objective requires to search for leads on Companies that require software development services in Australia with a specific company size, we'll apply filters relevant to companies first.

    Company Tab Filters:
    1. # Employees: "20-100" - This specifies the company size range.
    2. Industry & Keywords: Include industry keywords - 'computer software', 'information technology & services'. Including these keywords targets companies that are either offering or likely in need of these services. Exclude - "Social Media" = Excluding this targets companies keywords that are excluded.
    3. Account Location: "Australia" - To ensure only companies located in Australia are considered.


    People Tab Filters:
    For general points of contact, we typically look for job titles such as:

    1. Job Titles (General):
       - CEO/Managing Director - For smaller-sized businesses within the specified employee range.
       - General Manager - Often handles multiple roles including external communications in mid-sized firms.
       - Business Development Manager - Typically responsible for seeking new opportunities and partnerships which would include software development services.

    Number of results to export : 200

    Login Credentials : 
    - Email: notyouremail@email.com 
    - Password : Notyourpassword123


    FLOW OF ACTIONS::
    Given these requirements, here's how you'd proceed:
    !@#delim#@!

    Login into apollo using the credentials for email as 'notyouremail@email.com', and password as 'Notyourpassword123'
    1.Go to Companies tab.
    2.Choose # Employees filter and set it to range between '20-100' employees.
    3.Select Industry & Keywords and include industry keywords as 'computer software', 'information technology & services'. Exclude keywords as 'Social Media'.
    4.Set Account Location as 'Australia'.
    5.Apply filters for current selection.

    Then move to People tab and:
    6.Select Job Title by choosing titles like 'CEO/Managing Director', 'General Manager', or 'Business Development Manager'.

    After applying all selected filters across both tabs ensuring relevance and location specificity:

    Export the 200 results by selecting custom number of results to export which have populated on the page only after all selected filters are applied.

    Note: Complete all steps in each filter before proceeding to the next filter for accurate results


    EXAMPLE 4:
    Objective : Give me the list of 15 directors and managers working in companies in the gym and sports industry which are looking to hiring web developers and engineers. Login using the email and password as notfakeemail@somemail.com and Notfakepassword@12345 respectively.
    Response : Based on the objective given, here's the information extracted for filtering:

    Industry & Keywords:
    Include -
    (Industry Keywords)
    health, wellness & fitness
    sports
    (Company keywords)
    Gym
    Sports Industry

    Job Postings:
    Web Developers
    Engineers

    Job Titles:
    Directors
    Managers
    Given this information, we'll apply filters relevant to the companies first and then move on to the People tab.

    Number of results to export : 15

    Login Credentials : 
    - Email: notfakeemail@somemail.com 
    - Password : Notfakepassword@12345

    FLOW OF ACTIONS::
    Here's how you'd proceed:
    !@#delim#@!

    Login into apollo using the credentials for email as 'notfakeemail@somemail.com', and password as 'Notfakepassword@12345'
    1.Go to Companies tab.
    2.Select Industry & Keywords and include industry keywords as 'health, wellness & fitness', 'sports' and include company keywords as 'Gym', 'Sports Industry'.
    3.Select Job Postings filter and choose job titles such as 'Web Developers' and 'Engineers' to target companies looking to hire for these roles.

    Then move to People tab and:
    4.Select Job Titles and input titles 'Directors' and 'Managers'.

    After applying all selected filters across both tabs ensuring industry relevance and job title specificity:

    Export the list of 15 directors and managers by selecting custom number of results to export which have populated on the page only after all selected filters are applied.

    Note: Complete all steps in each filter before proceeding to the next filter for accurate results.

    Objective : {objective} 



Follow this structure to ensure your response is clear, detailed, and easy to follow. Make sure to always respond with the detailed action plan at all times.

    """
