# Archive class specialization for Gemini Observatory archive
# 
# This module defines a new class (GeminiArchive) derived from the 
# BasicArchive class, to allow queries to the Gemini Observatory Archive.


import urllib2, json, collections, math
import basic_archive, utils, archive_analyze

BROWSER_MASQUERADE = "Mozilla/5.0 [en]"

UNSPECIFIED_DEC_STRING = "-99.0"


# Gemini Observatory Archive:
TARGET_LABEL = "tobject"   # not used, but needed for basic_archive interface
RA_LABEL = "ra"            # not used, but needed for basic_archive interface
DEC_LABEL = "dec"          # not used, but needed for basic_archive interface
ARCHIVE_NAME = "Gemini Observatory Archive"
ARCHIVE_SHORTNAME = "gemini"
ARCHIVE_URL = "https://archive.gemini.edu/jsonsummary/canonical/science/NotTwilight/NotFail"
ARCHIVE_USER_URL = "https://archive.gemini.edu/searchform"


DICT = {}


# Code to parse HTML text and count up instrument uses

def FindObsModes( inputText, nFound=None ):
	# parse JSON
	filesList = json.loads(inputText)
	modeNameList = [f['mode'] for f in filesList]
	modeCountList = collections.Counter(modeNameList).items()

	nSets = len(modeCountList)
	msgText = "\n\t\t"
	if nSets > 1:
		for i in range(nSets - 1):
			msgText += "%d %s, " % (modeCountList[i][1], modeCountList[i][0])
	msgText += "%d %s" % (modeCountList[-1][1], modeCountList[-1][0])

	return msgText

def FindInstruments( inputText, nFound=None ):
	# parse JSON
	filesList = json.loads(inputText)
	instNameList = [f['instrument'] for f in filesList]
	instCountList = collections.Counter(instNameList).items()

	nSets = len(instCountList)
	msgText = "\n\t\t"
	if nSets > 1:
		for i in range(nSets - 1):
			msgText += "%s (%d), " % (instCountList[i][0], instCountList[i][1])
	msgText += "%s (%d)" % (instCountList[-1][0], instCountList[-1][1])

	return msgText


# Put all the functions in a list:
SEARCHES = [FindObsModes, FindInstruments]


# Subclass the BasicArchive class to handle deviant input and posting 
# requirements of the Gemini archive
class GeminiArchive(basic_archive.BasicArchive):

	def __init__( self, long_name, short_name, url, params_dict,
					specialSearches, targetLabel, raLabel, decLabel,
					special_params=None, boxLabel='box', publicURL=None ):
		super(GeminiArchive, self).__init__(long_name, short_name, url, params_dict,
										specialSearches, targetLabel, raLabel, decLabel, 
										special_params, boxLabel, publicURL)
		self.box_size_deg = 0.0667
		self.ra_string = "0.0"
		self.dec_string = UNSPECIFIED_DEC_STRING
		self.ra_decimal = -1.0
		self.dec_decimal = -100.0
	

	# Override the InsertBoxSize() method, because Gemini wants box size in degrees
	def InsertBoxSize( self, box_size ):
		self.box_size_deg = box_size / 60.0

	def InsertCoordinates( self, coords_list ):
		# coords_list is a two-element list of strings; each string must
		# be in the usual "hh mm ss.s" format, though decimal values are optional.
		#    Overriden for Gemini searches, which are easier with decimal degrees!
		ra_str = coords_list[0]
		dec_str = coords_list[1]
		ra_decimal, dec_decimal = utils.RADecToDecimalDeg(ra_str, dec_str)
		self.ra_decimal = float(ra_decimal)
		self.dec_decimal = float(dec_decimal)
		self.ra_string = ra_decimal
		self.dec_string = dec_decimal

	def MakeRADecRange( self ):
		"""Utility function to generate RA and Dec ranges for the search in
		Gemini Observatory Archive format, using the requested box size.
		"""
		halfWidth = self.box_size_deg / 2.0
		scaleFactor = math.cos(math.radians(self.dec_decimal))
		ra_min = self.ra_decimal - halfWidth/scaleFactor
		ra_max = self.ra_decimal + halfWidth/scaleFactor
		dec_min = self.dec_decimal - halfWidth
		dec_max = self.dec_decimal + halfWidth
		txt = "ra=%.7f-%.7f/dec=%.7f-%.7f" % (ra_min,ra_max,dec_min,dec_max)
		return txt
		
	# We override QueryServer because the Gemini Observatory Archive prefers 
	# options as a series of /-separated items
	def QueryServer( self ):
		# Opens connection to the archive server, retrieves and returns
		# whatever HTML the server sends us.

		self.URL_request = self.URL + "/" + self.MakeRADecRange()
		req = urllib2.Request(self.URL_request)
		req.add_header('User-agent', BROWSER_MASQUERADE)
		response = urllib2.urlopen(req, timeout=self.timeout)
		htmlReceived = response.read()
		response.close()

		return htmlReceived


	def AnalyzeHTML( self, htmlText ):
	
		# check for possible errors
		errMessage = archive_analyze.CheckForError(htmlText)
		if errMessage != "":
			return (errMessage, 0)
		
		# Search for possible observations
		# parse JSON text
		jsonList = json.loads(htmlText)
		nDataFound = len(jsonList)
		if ( nDataFound > 0 ):
			if nDataFound == 1:
				nSetsString = "One observation"
			else:
				nSetsString = "%d observations found" % nDataFound
			messageString = "Data exists! " + "(" + nSetsString + ")"
		else:
			messageString = "No data found."
		
		return (messageString, nDataFound)


# Factory function to create an instance of GeminiArchive
# Note that for this archive, we have a different label for the search box
# size.
def MakeArchive():
	return GeminiArchive(ARCHIVE_NAME, ARCHIVE_SHORTNAME, 
			ARCHIVE_URL, DICT, SEARCHES, TARGET_LABEL, RA_LABEL, DEC_LABEL,
			boxLabel="box")

