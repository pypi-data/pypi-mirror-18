# Archive class specialization for CFHT archive
# 
# This module defines a new class (CFHTArchive) derived from the 
# BasicArchive class, to allow queries to the archive of the Canada-France-
# Hawaii Telescope.

# The new class includes a modified QueryServer() method which uses 
# multipart/form posting (tests show that, unlike the case for the Gemini 
# archive), old-fashioned GET apparently still works for the CFHT archive 
# server; but since the default approach implemented by the current web page
# uses multipart/form, we'll use that.

import re
import basic_archive, multipart_form

DEFAULT_TARGET = "No Target"
DEFAULT_BOXSIZE_STRING = "00 04 00"
MAX_ROWS_RETURNED = "5000"

# Canada-France-Hawaii Telescope archive (Canada):
TARGET_LABEL = "tobject"
RA_LABEL = "ra"
DEC_LABEL = "dec"
ARCHIVE_NAME = "CFHT Archive"
ARCHIVE_SHORTNAME = "cfht"
ARCHIVE_URL = "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/AdvancedSearch/find"

# POST /AdvancedSearch/find sort_column=Start+Date&sort_order=descending&formName=adsform&SelectList=Observation.observationURI+AS+%22Preview%22%2C+Observation.collection+AS+%22Collection%22%2C+Observation.sequenceNumber+AS+%22Sequence+Number%22%2C+Plane.productID+AS+%22Product+ID%22%2C+COORD1(CENTROID(Plane.position_bounds))+AS+%22RA+(J2000.0)%22%2C+COORD2(CENTROID(Plane.position_bounds))+AS+%22Dec.+(J2000.0)%22%2C+Observation.target_name+AS+%22Target+Name%22%2C+Plane.time_bounds_cval1+AS+%22Start+Date%22%2C+Plane.time_exposure+AS+%22Int.+Time%22%2C+Observation.instrument_name+AS+%22Instrument%22%2C+Plane.energy_bandpassName+AS+%22Filter%22%2C+Plane.calibrationLevel+AS+%22Cal.+Lev.%22%2C+Observation.type+AS+%22Obs.+Type%22%2C+Observation.proposal_id+AS+%22Proposal+ID%22%2C+Observation.proposal_pi+AS+%22P.I.+Name%22%2C+Plane.dataRelease+AS+%22Data+Release%22%2C+Observation.observationID+AS+%22Obs.+ID%22%2C+Plane.energy_bounds_cval1+AS+%22Min.+Wavelength%22%2C+Plane.energy_bounds_cval2+AS+%22Max.+Wavelength%22%2C+AREA(Plane.position_bounds)+AS+%22Field+of+View%22%2C+Plane.position_sampleSize+AS+%22Pixel+Scale%22%2C+Plane.energy_resolvingPower+AS+%22Resolving+Power%22%2C+Plane.dataProductType+AS+%22Data+Type%22%2C+Observation.target_moving+AS+%22Moving+Target%22%2C+Plane.provenance_name+AS+%22Provenance+Name%22%2C+Observation.intent+AS+%22Intent%22%2C+Observation.target_type+AS+%22Target+Type%22%2C+Observation.target_standard+AS+%22Target+Standard%22%2C+Observation.algorithm_name+AS+%22Algorithm+Name%22%2C+Observation.proposal_title+AS+%22Proposal+Title%22%2C+Observation.proposal_keywords+AS+%22Proposal+Keywords%22%2C+Plane.position_resolution+AS+%22IQ%22%2C+Observation.instrument_keywords+AS+%22Instrument+Keywords%22%2C+Plane.energy_transition_species+AS+%22Molecule%22%2C+Plane.energy_transition_transition+AS+%22Transition%22%2C+Plane.energy_emBand+AS+%22Band%22%2C+Plane.provenance_version+AS+%22Prov.+Version%22%2C+Plane.provenance_project+AS+%22Prov.+Project%22%2C+Plane.provenance_runID+AS+%22Prov.+Run+ID%22%2C+Plane.provenance_lastExecuted+AS+%22Prov.+Last+Executed%22%2C+Plane.energy_restwav+AS+%22Rest-frame+Energy%22%2C+Observation.requirements_flag+AS+%22Quality%22%2C+isDownloadable(Plane.planeURI)+AS+%22DOWNLOADABLE%22%2C+Plane.planeURI+AS+%22CAOM+Plane+URI%22&MaxRecords=30000&format=csv&Observation.observationID=&Form.name=Observation.observationID%40Text&Observation.proposal.pi=&Form.name=Observation.proposal.pi%40Text&Observation.proposal.id=&Form.name=Observation.proposal.id%40Text&Observation.proposal.title=&Form.name=Observation.proposal.title%40Text&Observation.proposal.keywords=&Form.name=Observation.proposal.keywords%40Text&Plane.dataRelease=&Form.name=Plane.dataRelease%40TimestampFormConstraint&Form.name=Plane.dataRelease%40PublicTimestampFormConstraint&Observation.intent=&Form.name=Observation.intent%40Text&Plane.position.bounds%40Shape1Resolver.value=ALL&Plane.position.bounds%40Shape1.value=210.05+54.3+0.5&targetList=&Form.name=targetList.targetList&Form.name=Plane.position.bounds%40Shape1&Plane.position.sampleSize=&Form.name=Plane.position.sampleSize%40Number&Form.name=Plane.position.DOWNLOADCUTOUT%40Boolean&Plane.time.bounds%40Date.value=&Plane.time.bounds_PRESET%40Date.value=&Form.name=Plane.time.bounds%40Date&Plane.time.exposure=&Form.name=Plane.time.exposure%40Number&Plane.time.bounds.width=&Form.name=Plane.time.bounds.width%40Number&Plane.energy.bounds%40Energy.value=&Form.name=Plane.energy.bounds%40Energy&Plane.energy.sampleSize=&Form.name=Plane.energy.sampleSize%40Number&Plane.energy.resolvingPower=&Form.name=Plane.energy.resolvingPower%40Number&Plane.energy.bounds.width=&Form.name=Plane.energy.bounds.width%40Number&Plane.energy.restwav=&Form.name=Plane.energy.restwav%40Number&Form.name=Plane.energy.DOWNLOADCUTOUT%40Boolean&Form.name=Plane.energy.emBand%40Enumerated&Form.name=Observation.collection%40Enumerated&Form.name=Observation.instrument.name%40Enumerated&Form.name=Plane.energy.bandpassName%40Enumerated&Form.name=Plane.calibrationLevel%40Enumerated&Form.name=Plane.dataProductType%40Enumerated&Form.name=Observation.type%40Enumerated&Plane.energy.emBand=&Observation.collection=CFHT&Observation.instrument.name=&Plane.energy.bandpassName=&Plane.calibrationLevel=&Plane.dataProductType=&Observation.type=

ARCHIVE_USER_URL = "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/search/?collection=CFHT&noexec=true"
DICT = {TARGET_LABEL: DEFAULT_TARGET, 
		RA_LABEL: "", DEC_LABEL: "",
		'wdbi_order': "",
		'tobject': "",
		'simbad': "simbad",
		'max_rows_returned': MAX_ROWS_RETURNED,
		'box': DEFAULT_BOXSIZE_STRING,
		'expnum': "",
		'tab_instrument': "on",
		'instrument': "%",
		'exposure': "",
		'filter': "",
		'photometric': "%",
		'creation_date': "",
		'release_date': "",
		'runid': "",
		'obstype': "OBJECT",
		'category': "%"
		}


# Code to parse HTML text and count up instrument uses

# the following RE object searches for instances of table entries referring to
# instruments and stores the actual instrument name
# text to search for in order to find/count instruments:
#      <input type="hidden" name="Instrument" value="*instrument-name*">
# e.g.,
#      <input type="hidden" name="Instrument" value="HRC">
findInstruments = re.compile(r"""<input type="hidden" name="Instrument" value="([^"]+?)">""")

def FindInstruments(inputText, nFound=None):
	foundStuff = findInstruments.findall(inputText)
	theDict = {}
	instList = []
	for item in foundStuff:
		if item not in instList:
			theDict[item] = 1
			instList.append(item)
		else:
			theDict[item] += 1

	msgText = "\n\t\t"
	for i in range(len(instList)):
		instName = instList[i]
		msgText += instName + " (%d)" % theDict[instName]
		if (i < (len(instList) - 1)):
			msgText += ", "
	
	return msgText

# Put all the functions in a list:
SEARCHES = [FindInstruments]


# Subclass the BasicArchive class to handle deviant input and posting 
# requirements of the CFHT archive
class CFHTArchive(basic_archive.BasicArchive):

	# We override QueryServer because the CFHT Archive prefers 
	# multipart/form-data queries, not urlencoded
	def QueryServer(self):
		# Opens connection to the archive server, retrieves and returns
		# whatever HTML the server sends us.
		# Note that here we are using our special multipart/form-data
		# method for posting to the archive.
		connection = multipart_form.MultipartPost(self.URL, self.params)
		# Loop to make sure we get *all* of the HTML (bug of sorts in MacPython 2.0--2.2):
		htmlReceived = ''
		newdata = connection.read()
		while newdata:
			htmlReceived += newdata
			newdata = connection.read()
		connection.close()
		return htmlReceived


# Factory function to create an instance of CFHTArchive
# Note that for this archive, we have a different label for the search box
# size.
def MakeArchive():
	return CFHTArchive(ARCHIVE_NAME, ARCHIVE_SHORTNAME, 
			ARCHIVE_URL, DICT, SEARCHES, TARGET_LABEL, RA_LABEL, DEC_LABEL,
			boxLabel="box")

