from watson_developer_cloud import AssistantV1

log_list = [
	"cancel the order",
	"change, cancel please",
	"nevermin, just cancel",
	"are you guys open during xmas",
	"when do you guys close?",
	"can i call at night?",
	"are u guys opened friday?",
	"are you opened on sundays?",
	"do you close late?",
	"do you open early?",
	"will you open tomorrow?",
	"i need some help please",
	"can someone help me?",
	"help, i need somebody help, not just anybody...",
	"for the love of god someone help me",
	"can someone help me decide what i need?",
	"can anyone help me on my MIPS?",
	"im neckless, need help to use necklace?",
	"can you help me become a better bodybuilder?",
	"call mister python the manager, the best manager",
	"please send a manager",
	"i need to speak to a manager",
	"contact master kid musculo",
]

assistant = AssistantV1(
    version='2018-09-20',
    username='3ceb2604-5436-49f0-9d6e-f15ba1215cd9',
    password='Lbj3hbZwRJXD',
    url='https://gateway.watsonplatform.net/assistant/api'
)

for log in log_list:
	assistant.message(
	    workspace_id='b903d94d-7fb0-4309-a84b-543d261a2f08',
	    input={
	        'text': log
	    }
	)