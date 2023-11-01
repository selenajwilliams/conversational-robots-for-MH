# conversational-robots-for-MH
Spring '23 Research Project in Brown's Humans to Robots Lab

## Problem Space
Mental health has been declared an unprecedented national crisis amidst a severe shortage of mental health providers and a fragmented healthcare system (Whitehouse.gov). Mental health issues are on the rise globally causing 1 in every 5 years lived in disability and more than $1 trillion annually (WHO). The rise of mental health issues and lack of labor force to address this need is happening amidst an AI revolution ripe with opportunities for technological innovation to advance, treat, and support public mental health.

So far, little research has been done to measure the potential that LLMs and robots can have to support mental health in complement to traditional therapy and MH services. Given the national shortage of providers, growing burden of national mental health, and promise of these technologies in other spaces, this project explores the impact that an LLM-equipped home robot (Kuri) can play in supporting user emotional wellbeing by role-playing as a peer support counselor. 


## Opportunties to Improve LLM Performance:
1. Introduce model finetuning
    article:
2. Introduce a way for the model to summarize past comments in the conversation
    * This will help minimize the tokens used (reduce overall system cost) and improve the model performance. Currently the system is not explicitly including prior user input and LLM response and I'm not sure if it will do that implicitly/automatically
3. Introduce more empathetic responses through **sentiment analysis** enabling the system to respond in a way that reflects the user emotion 
    * This could be either by: 
        * telling the model to 'respond in a [user_emotion], empathetic way' OR
        * telling the model to 'respond in a way that supports someone experiencing [user_emotion]'

## Testing Plan
Goals: 
* Conduct qualitative pilot studies with lab by end of semester
* Conduct quantiative studies with participants next semester

User Study Outline For Quantiative Study Spring 2024:
Have users fill out a standard, clinical wellbeing/emotion assessment and NARS (Negative Attitudes towards Robots Survey) before and after interacting with the system
Have 3 non-clinical interventions that users are randomly allocated to: embodied LLM system (this system in Kuri), digital LLM system (this system accessible through a webapp), and a low-tech wellbeing activity like journaling (possibly synced with similar prompts that all systems can ask)
Have all users fill out the assessments noted above before & after and measure outcomes to see which system most helps users with their emotional and overall wellbeing