from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import requests

# corda api definitions
nodeAddress = "http://localhost"
apiVault = "api/example/ious"
apiCreateIOU = "api/example/create-iou?iouValue="
apiPeers = "api/example/peers"
apiMe = "api/example/me"

def createIOU(request, hostport):
	port = ":" + hostport + "/"
	target = request.POST['target']
	targetamount = request.POST['value']
	r = requests.put(nodeAddress + port +
		apiCreateIOU + targetamount + "&partyName=" + target)
	return HttpResponseRedirect(reverse('trade:detail', args=([hostport])))

#string parsers
def peerParse(astr):
	party1 = astr[2:astr.find(",")]
	location1 = astr[astr.find(",") + 4 : astr.find(",", astr.find(",") + 1)]
	country1 = astr[astr.find("C=") + 2:]
	peer = party1 + ", " + location1 + ", " + country1
	return(peer, party1, location1, country1)

def listLogs(alist, ajson):  #parses ajson into alist of formatted strings
	for i in ajson:
		value = i['state']['data']['value']
		borrower = str(peerParse(i['state']['data']['borrower'])[0])
		alist.append(borrower + " owing SGD" + str(value))

def total(x):
	totalB = 0
	totalC = 0
	for i in x:
		if i.startswith("PartyB"):
			totalB = totalB + int(i.split(" ")[5][3:])
		elif i.startswith("PartyC"):
			totalC = totalC + int(i.split(" ")[4][3:])
	return(totalB, totalC)

# views
def index(request):
	return(render(request, 'trade/index.html'))

def detail(request, hostport):
	port = ":" + hostport + "/"
	rvault = requests.get(nodeAddress + port + apiVault).json()
	rme = requests.get(nodeAddress + port + apiMe).json()['me']
	rpeers = requests.get(nodeAddress + port + apiPeers).json()['peers']
	peer1, p1, l1, c1 = peerParse(rpeers[0])
	peer2, p2, l2, c2 = peerParse(rpeers[1])
	peer1path = "O="+p1+",L="+l1.replace(" ", "%20")+",C="+c1
	peer2path = "O="+p2+",L="+l2.replace(" ", "%20")+",C="+c2
	print(l1)
	print(l2)
	vaultRow = []
	listLogs(vaultRow, rvault)
	totalB, totalC = total(vaultRow)
	return render(request, 'trade/detail.html', {
		'rends':vaultRow, 'totalB':totalB, 
		'totalC':totalC, 'hostport': hostport,
		'peer1': l1,
		'peer2': l2,
		'peer1path': peer1path,
		'peer2path': peer2path,
		'me': peerParse(rme)[2]
		})