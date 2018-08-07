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

# HTTP put request to corda network
def createIOU(request, hostport):
	port = ":" + hostport + "/"
	target = request.POST['target']
	targetamount = request.POST['value']
	r = requests.put(nodeAddress + port +
		apiCreateIOU + targetamount + "&partyName=" + target)
	return HttpResponseRedirect(reverse('trade:detail', args=([hostport])))

# json parsers
def peerParse(astr): #parses a corda identifier string
	party1 = astr[2:astr.find(",")]
	location1 = astr[astr.find(",") + 4 : astr.find(",", astr.find(",") + 1)]
	country1 = astr[astr.find("C=") + 2:]
	peer = party1 + ", " + location1 + ", " + country1
	return(peer, party1, location1, country1)

# Parses a raw vault json into a list of dictionaries, 1dict per ledger entry


# views
def index(request):
	return(render(request, 'trade/index.html'))

def detail(request, hostport):

	# HTTP Requests relative to hostport rovided in URL
	port = ":" + hostport + "/"
	rvault = requests.get(nodeAddress + port + apiVault).json()
	rme = requests.get(nodeAddress + port + apiMe).json()['me']
	rpeers = requests.get(nodeAddress + port + apiPeers).json()['peers']

	def jsonParse(aledger):
		alist = []
		balance1 = 0
		balance2 = 0
		balance3 = 0
		balance4 = 0
		for entry in aledger:
			transactionID = entry['ref']['txhash']
			value = entry['state']['data']['value']
			lenderName = peerParse(entry['state']['data']['lender'])[1]
			lenderLocation = peerParse(entry['state']['data']['lender'])[2]
			lenderCountry = peerParse(entry['state']['data']['lender'])[3]
			borrowerName = peerParse(entry['state']['data']['borrower'])[1]
			borrowerLocation = peerParse(entry['state']['data']['borrower'])[2]
			borrowerCountry = peerParse(entry['state']['data']['borrower'])[3]

			# Adds up total owed and owing by parties related to current host
			if lenderLocation == peerParse(rpeers[0])[2] and borrowerLocation == peerParse(rme)[2]:
				balance1 = balance1 + value
			elif lenderLocation == peerParse(rpeers[1])[2] and borrowerLocation == peerParse(rme)[2]:
				balance2 = balance2 + value
			elif lenderLocation == peerParse(rme)[2] and borrowerLocation == peerParse(rpeers[0])[2]:
				balance3 = balance3 + value
			elif lenderLocation == peerParse(rme)[2] and borrowerLocation == peerParse(rpeers[1])[2]:
				balance4 = balance4 + value

			parsedDict = {
			'transactionID':transactionID, 'lenderName':lenderName, 
			'lenderLocation':lenderLocation, 'lenderCountry':lenderCountry,
			'borrowerName':borrowerName,'borrowerLocation':borrowerLocation,
			'borrowerCountry':borrowerCountry, 'value': value, 'balance1':balance1,
			'balance2':balance2, 'balance3':balance3, 'balance4':balance4}

			alist.append(parsedDict)
		return(alist)

	# Dictionary assosciations returned to template for web page rendering
	peer1, p1, l1, c1 = peerParse(rpeers[0])
	peer2, p2, l2, c2 = peerParse(rpeers[1])

	# Construct HTTP calls in Corda IOU submission format 
	peer1path = "O="+p1+",L="+l1.replace(" ", "%20")+",C="+c1
	peer2path = "O="+p2+",L="+l2.replace(" ", "%20")+",C="+c2

	return render(request, 'trade/detail.html', {
		'rends':list(reversed(jsonParse(rvault))), 
		'hostport': hostport,
		'peer1': l1, 'peer2': l2,
		'peer1path': peer1path,
		'peer2path': peer2path,
		'me': peerParse(rme)[2]
		})