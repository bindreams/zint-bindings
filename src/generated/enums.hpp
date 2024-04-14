/// This file was generated automatically by scripts/generate-enums.py. Please do not edit it manually.
#pragma once
#include <pybind11/pybind11.h>

namespace py = pybind11;

enum class Symbology : int {
	CODE11 = 1,
	C25STANDARD = 2,
	C25INTER = 3,
	C25IATA = 4,
	C25LOGIC = 6,
	C25IND = 7,
	CODE39 = 8,
	EXCODE39 = 9,
	EANX = 13,
	EANX_CHK = 14,
	GS1_128 = 16,
	CODABAR = 18,
	CODE128 = 20,
	DPLEIT = 21,
	DPIDENT = 22,
	CODE16K = 23,
	CODE49 = 24,
	CODE93 = 25,
	FLAT = 28,
	DBAR_OMN = 29,
	DBAR_LTD = 30,
	DBAR_EXP = 31,
	TELEPEN = 32,
	UPCA = 34,
	UPCA_CHK = 35,
	UPCE = 37,
	UPCE_CHK = 38,
	POSTNET = 40,
	MSI_PLESSEY = 47,
	FIM = 49,
	LOGMARS = 50,
	PHARMA = 51,
	PZN = 52,
	PHARMA_TWO = 53,
	CEPNET = 54,
	PDF417 = 55,
	PDF417COMP = 56,
	MAXICODE = 57,
	QRCODE = 58,
	CODE128AB = 60,
	AUSPOST = 63,
	AUSREPLY = 66,
	AUSROUTE = 67,
	AUSREDIRECT = 68,
	ISBNX = 69,
	RM4SCC = 70,
	DATAMATRIX = 71,
	EAN14 = 72,
	VIN = 73,
	CODABLOCKF = 74,
	NVE18 = 75,
	JAPANPOST = 76,
	KOREAPOST = 77,
	DBAR_STK = 79,
	DBAR_OMNSTK = 80,
	DBAR_EXPSTK = 81,
	PLANET = 82,
	MICROPDF417 = 84,
	USPS_IMAIL = 85,
	PLESSEY = 86,
	TELEPEN_NUM = 87,
	ITF14 = 89,
	KIX = 90,
	AZTEC = 92,
	DAFT = 93,
	DPD = 96,
	MICROQR = 97,
	HIBC_128 = 98,
	HIBC_39 = 99,
	HIBC_DM = 102,
	HIBC_QR = 104,
	HIBC_PDF = 106,
	HIBC_MICPDF = 108,
	HIBC_BLOCKF = 110,
	HIBC_AZTEC = 112,
	DOTCODE = 115,
	HANXIN = 116,
	MAILMARK_2D = 119,
	UPU_S10 = 120,
	MAILMARK_4S = 121,
	AZRUNE = 128,
	CODE32 = 129,
	EANX_CC = 130,
	GS1_128_CC = 131,
	DBAR_OMN_CC = 132,
	DBAR_LTD_CC = 133,
	DBAR_EXP_CC = 134,
	UPCA_CC = 135,
	UPCE_CC = 136,
	DBAR_STK_CC = 137,
	DBAR_OMNSTK_CC = 138,
	DBAR_EXPSTK_CC = 139,
	CHANNEL = 140,
	CODEONE = 141,
	GRIDMATRIX = 142,
	UPNQR = 143,
	ULTRA = 144,
	RMQR = 145,
	BC412 = 146
};
enum class OutputOptions : int {
	BARCODE_BIND_TOP = 1,
	BARCODE_BIND = 2,
	BARCODE_BOX = 4,
	BARCODE_STDOUT = 8,
	READER_INIT = 16,
	SMALL_TEXT = 32,
	BOLD_TEXT = 64,
	CMYK_COLOUR = 128,
	BARCODE_DOTTY_MODE = 256,
	GS1_GS_SEPARATOR = 512,
	OUT_BUFFER_INTERMEDIATE = 1024,
	BARCODE_QUIET_ZONES = 2048,
	BARCODE_NO_QUIET_ZONES = 4096,
	COMPLIANT_HEIGHT = 8192,
	EANUPC_GUARD_WHITESPACE = 16384,
	EMBED_VECTOR_FONT = 32768,
	BARCODE_MEMORY_FILE = 65536
};
enum class InputMode : int {
	DATA = 0,
	UNICODE = 1,
	GS1 = 2,
	ESCAPE = 8,
	GS1PARENS = 16,
	GS1NOCHECK = 32,
	HEIGHTPERROW = 64,
	FAST = 128,
	EXTRA_ESCAPE = 256
};
enum class DataMatrixOptions : int { SQUARE = 100, DMRE = 101, ISO_144 = 128 };
enum class QrFamilyOptions : int { FULL_MULTIBYTE = 200 };
enum class UltracodeOptions : int { ULTRA_COMPRESSION = 128 };
enum class WarningLevel : int { DEFAULT = 0, FAIL_ALL = 2 };
enum class CapabilityFlags : unsigned int {
	HRT = 1,
	STACKABLE = 2,
	EANUPC = 4,
	EXTENDABLE = 4,
	COMPOSITE = 8,
	ECI = 16,
	GS1 = 32,
	DOTTY = 64,
	QUIET_ZONES = 128,
	FIXED_RATIO = 256,
	READER_INIT = 512,
	FULL_MULTIBYTE = 1024,
	MASK = 2048,
	STRUCTAPP = 4096,
	COMPLIANT_HEIGHT = 8192
};

inline void init_enum_bindings(pybind11::module_& m) {
	py::enum_<Symbology>(m, "Symbology", "Values for `Symbol.symbology`")
		.value("CODE11", Symbology::CODE11, "Code 11")
		.value("C25STANDARD", Symbology::C25STANDARD, "2 of 5 Standard (Matrix)")
		.value("C25INTER", Symbology::C25INTER, "2 of 5 Interleaved")
		.value("C25IATA", Symbology::C25IATA, "2 of 5 IATA")
		.value("C25LOGIC", Symbology::C25LOGIC, "2 of 5 Data Logic")
		.value("C25IND", Symbology::C25IND, "2 of 5 Industrial")
		.value("CODE39", Symbology::CODE39, "Code 39")
		.value("EXCODE39", Symbology::EXCODE39, "Extended Code 39")
		.value("EANX", Symbology::EANX, "EAN (European Article Number)")
		.value("EANX_CHK", Symbology::EANX_CHK, "EAN + Check Digit")
		.value("GS1_128", Symbology::GS1_128, "GS1-128")
		.value("CODABAR", Symbology::CODABAR, "Codabar")
		.value("CODE128", Symbology::CODE128, "Code 128")
		.value("DPLEIT", Symbology::DPLEIT, "Deutsche Post Leitcode")
		.value("DPIDENT", Symbology::DPIDENT, "Deutsche Post Identcode")
		.value("CODE16K", Symbology::CODE16K, "Code 16k")
		.value("CODE49", Symbology::CODE49, "Code 49")
		.value("CODE93", Symbology::CODE93, "Code 93")
		.value("FLAT", Symbology::FLAT, "Flattermarken")
		.value("DBAR_OMN", Symbology::DBAR_OMN, "GS1 DataBar Omnidirectional")
		.value("DBAR_LTD", Symbology::DBAR_LTD, "GS1 DataBar Limited")
		.value("DBAR_EXP", Symbology::DBAR_EXP, "GS1 DataBar Expanded")
		.value("TELEPEN", Symbology::TELEPEN, "Telepen Alpha")
		.value("UPCA", Symbology::UPCA, "UPC-A")
		.value("UPCA_CHK", Symbology::UPCA_CHK, "UPC-A + Check Digit")
		.value("UPCE", Symbology::UPCE, "UPC-E")
		.value("UPCE_CHK", Symbology::UPCE_CHK, "UPC-E + Check Digit")
		.value("POSTNET", Symbology::POSTNET, "USPS (U.S. Postal Service) POSTNET")
		.value("MSI_PLESSEY", Symbology::MSI_PLESSEY, "MSI Plessey")
		.value("FIM", Symbology::FIM, "Facing Identification Mark")
		.value("LOGMARS", Symbology::LOGMARS, "LOGMARS")
		.value("PHARMA", Symbology::PHARMA, "Pharmacode One-Track")
		.value("PZN", Symbology::PZN, "Pharmazentralnummer")
		.value("PHARMA_TWO", Symbology::PHARMA_TWO, "Pharmacode Two-Track")
		.value("CEPNET", Symbology::CEPNET, "Brazilian CEPNet Postal Code")
		.value("PDF417", Symbology::PDF417, "PDF417")
		.value("PDF417COMP", Symbology::PDF417COMP, "Compact PDF417 (Truncated PDF417)")
		.value("MAXICODE", Symbology::MAXICODE, "MaxiCode")
		.value("QRCODE", Symbology::QRCODE, "QR Code")
		.value("CODE128AB", Symbology::CODE128AB, "Code 128 (Suppress Code Set C)")
		.value("AUSPOST", Symbology::AUSPOST, "Australia Post Standard Customer")
		.value("AUSREPLY", Symbology::AUSREPLY, "Australia Post Reply Paid")
		.value("AUSROUTE", Symbology::AUSROUTE, "Australia Post Routing")
		.value("AUSREDIRECT", Symbology::AUSREDIRECT, "Australia Post Redirection")
		.value("ISBNX", Symbology::ISBNX, "ISBN")
		.value("RM4SCC", Symbology::RM4SCC, "Royal Mail 4-State Customer Code")
		.value("DATAMATRIX", Symbology::DATAMATRIX, "Data Matrix (ECC200)")
		.value("EAN14", Symbology::EAN14, "EAN-14")
		.value("VIN", Symbology::VIN, "Vehicle Identification Number")
		.value("CODABLOCKF", Symbology::CODABLOCKF, "Codablock-F")
		.value("NVE18", Symbology::NVE18, "NVE-18 (SSCC-18)")
		.value("JAPANPOST", Symbology::JAPANPOST, "Japanese Postal Code")
		.value("KOREAPOST", Symbology::KOREAPOST, "Korea Post")
		.value("DBAR_STK", Symbology::DBAR_STK, "GS1 DataBar Stacked")
		.value("DBAR_OMNSTK", Symbology::DBAR_OMNSTK, "GS1 DataBar Stacked Omnidirectional")
		.value("DBAR_EXPSTK", Symbology::DBAR_EXPSTK, "GS1 DataBar Expanded Stacked")
		.value("PLANET", Symbology::PLANET, "USPS PLANET")
		.value("MICROPDF417", Symbology::MICROPDF417, "MicroPDF417")
		.value("USPS_IMAIL", Symbology::USPS_IMAIL, "USPS Intelligent Mail (OneCode)")
		.value("PLESSEY", Symbology::PLESSEY, "UK Plessey")
		.value("TELEPEN_NUM", Symbology::TELEPEN_NUM, "Telepen Numeric")
		.value("ITF14", Symbology::ITF14, "ITF-14")
		.value("KIX", Symbology::KIX, "Dutch Post KIX Code")
		.value("AZTEC", Symbology::AZTEC, "Aztec Code")
		.value("DAFT", Symbology::DAFT, "DAFT Code")
		.value("DPD", Symbology::DPD, "DPD Code")
		.value("MICROQR", Symbology::MICROQR, "Micro QR Code")
		.value("HIBC_128", Symbology::HIBC_128, "HIBC (Health Industry Barcode) Code 128")
		.value("HIBC_39", Symbology::HIBC_39, "HIBC Code 39")
		.value("HIBC_DM", Symbology::HIBC_DM, "HIBC Data Matrix")
		.value("HIBC_QR", Symbology::HIBC_QR, "HIBC QR Code")
		.value("HIBC_PDF", Symbology::HIBC_PDF, "HIBC PDF417")
		.value("HIBC_MICPDF", Symbology::HIBC_MICPDF, "HIBC MicroPDF417")
		.value("HIBC_BLOCKF", Symbology::HIBC_BLOCKF, "HIBC Codablock-F")
		.value("HIBC_AZTEC", Symbology::HIBC_AZTEC, "HIBC Aztec Code")
		.value("DOTCODE", Symbology::DOTCODE, "DotCode")
		.value("HANXIN", Symbology::HANXIN, "Han Xin (Chinese Sensible) Code")
		.value("MAILMARK_2D", Symbology::MAILMARK_2D, "Royal Mail 2D Mailmark (CMDM) (Data Matrix)")
		.value("UPU_S10", Symbology::UPU_S10, "Universal Postal Union S10")
		.value("MAILMARK_4S", Symbology::MAILMARK_4S, "Royal Mail 4-State Mailmark")
		.value("AZRUNE", Symbology::AZRUNE, "Aztec Runes")
		.value("CODE32", Symbology::CODE32, "Code 32")
		.value("EANX_CC", Symbology::EANX_CC, "EAN Composite")
		.value("GS1_128_CC", Symbology::GS1_128_CC, "GS1-128 Composite")
		.value("DBAR_OMN_CC", Symbology::DBAR_OMN_CC, "GS1 DataBar Omnidirectional Composite")
		.value("DBAR_LTD_CC", Symbology::DBAR_LTD_CC, "GS1 DataBar Limited Composite")
		.value("DBAR_EXP_CC", Symbology::DBAR_EXP_CC, "GS1 DataBar Expanded Composite")
		.value("UPCA_CC", Symbology::UPCA_CC, "UPC-A Composite")
		.value("UPCE_CC", Symbology::UPCE_CC, "UPC-E Composite")
		.value("DBAR_STK_CC", Symbology::DBAR_STK_CC, "GS1 DataBar Stacked Composite")
		.value("DBAR_OMNSTK_CC", Symbology::DBAR_OMNSTK_CC, "GS1 DataBar Stacked Omnidirectional Composite")
		.value("DBAR_EXPSTK_CC", Symbology::DBAR_EXPSTK_CC, "GS1 DataBar Expanded Stacked Composite")
		.value("CHANNEL", Symbology::CHANNEL, "Channel Code")
		.value("CODEONE", Symbology::CODEONE, "Code One")
		.value("GRIDMATRIX", Symbology::GRIDMATRIX, "Grid Matrix")
		.value("UPNQR", Symbology::UPNQR, "UPNQR (Univerzalnega Plačilnega Naloga QR)")
		.value("ULTRA", Symbology::ULTRA, "Ultracode")
		.value("RMQR", Symbology::RMQR, "Rectangular Micro QR Code (rMQR)")
		.value("BC412", Symbology::BC412, "IBM BC412 (SEMI T1-95)");
	py::enum_<OutputOptions>(m, "OutputOptions", py::arithmetic{}, "Values for `Symbol.output_options`")
		.value(
			"BARCODE_BIND_TOP",
			OutputOptions::BARCODE_BIND_TOP,
			"Boundary bar above the symbol only (not below), does not affect stacking. Note: value was once used by "
			"the legacy (never-used) BARCODE_NO_ASCII"
		)
		.value(
			"BARCODE_BIND",
			OutputOptions::BARCODE_BIND,
			"Boundary bars above & below the symbol and between stacked symbols"
		)
		.value("BARCODE_BOX", OutputOptions::BARCODE_BOX, "Box around symbol")
		.value("BARCODE_STDOUT", OutputOptions::BARCODE_STDOUT, "Output to stdout")
		.value("READER_INIT", OutputOptions::READER_INIT, "Reader Initialisation (Programming)")
		.value("SMALL_TEXT", OutputOptions::SMALL_TEXT, "Use smaller font")
		.value("BOLD_TEXT", OutputOptions::BOLD_TEXT, "Use bold font")
		.value("CMYK_COLOUR", OutputOptions::CMYK_COLOUR, "CMYK colour space (Encapsulated PostScript and TIF)")
		.value(
			"BARCODE_DOTTY_MODE",
			OutputOptions::BARCODE_DOTTY_MODE,
			"Plot a matrix symbol using dots rather than squares"
		)
		.value(
			"GS1_GS_SEPARATOR", OutputOptions::GS1_GS_SEPARATOR, "Use GS instead of FNC1 as GS1 separator (Data Matrix)"
		)
		.value(
			"OUT_BUFFER_INTERMEDIATE",
			OutputOptions::OUT_BUFFER_INTERMEDIATE,
			"Return ASCII values in bitmap buffer (OUT_BUFFER only)"
		)
		.value(
			"BARCODE_QUIET_ZONES",
			OutputOptions::BARCODE_QUIET_ZONES,
			"Add compliant quiet zones (additional to any specified whitespace). Note: CODE16K, CODE49, CODABLOCKF, "
			"ITF14, EAN/UPC have default quiet zones"
		)
		.value(
			"BARCODE_NO_QUIET_ZONES",
			OutputOptions::BARCODE_NO_QUIET_ZONES,
			"Disable quiet zones, notably those with defaults as listed above"
		)
		.value(
			"COMPLIANT_HEIGHT",
			OutputOptions::COMPLIANT_HEIGHT,
			"Warn if height not compliant, or use standard height (if any) as default"
		)
		.value(
			"EANUPC_GUARD_WHITESPACE",
			OutputOptions::EANUPC_GUARD_WHITESPACE,
			"Add quiet zone indicators (\"<\"/\">\") to HRT whitespace (EAN/UPC)"
		)
		.value(
			"EMBED_VECTOR_FONT",
			OutputOptions::EMBED_VECTOR_FONT,
			"Embed font in vector output - currently only for SVG output"
		)
		.value(
			"BARCODE_MEMORY_FILE",
			OutputOptions::BARCODE_MEMORY_FILE,
			"Write output to in-memory buffer `memfile` instead of to `outfile`"
		);
	py::enum_<InputMode>(m, "InputMode", py::arithmetic{}, "Values for `Symbol.input_mode`")
		.value("DATA", InputMode::DATA, "Binary")
		.value("UNICODE", InputMode::UNICODE, "UTF-8")
		.value("GS1", InputMode::GS1, "GS1. The following may be OR-ed with above")
		.value("ESCAPE", InputMode::ESCAPE, "Process escape sequences")
		.value(
			"GS1PARENS", InputMode::GS1PARENS, "Process parentheses as GS1 AI delimiters (instead of square brackets)"
		)
		.value(
			"GS1NOCHECK", InputMode::GS1NOCHECK, "Do not check validity of GS1 data (except that printable ASCII only)"
		)
		.value("HEIGHTPERROW", InputMode::HEIGHTPERROW, "Interpret `height` as per-row rather than as overall height")
		.value(
			"FAST",
			InputMode::FAST,
			"Use faster if less optimal encodation or other shortcuts if available. Note: affects DATAMATRIX, "
			"MICROPDF417, PDF417, QRCODE & UPNQR only"
		)
		.value(
			"EXTRA_ESCAPE",
			InputMode::EXTRA_ESCAPE,
			"Process special symbology-specific escape sequences. Note: currently Code 128 only"
		);
	py::enum_<DataMatrixOptions>(m, "DataMatrixOptions", "Data Matrix specific options (`symbol->option_3`)")
		.value("SQUARE", DataMatrixOptions::SQUARE, "Only consider square versions on automatic symbol size selection")
		.value("DMRE", DataMatrixOptions::DMRE, "Consider DMRE versions on automatic symbol size selection")
		.value(
			"ISO_144",
			DataMatrixOptions::ISO_144,
			"Use ISO instead of \"de facto\" format for 144x144 (i.e. don't skew ECC)"
		);
	py::enum_<QrFamilyOptions>(m, "QrFamilyOptions", "QR, Han Xin, Grid Matrix specific options (`symbol->option_3`)")
		.value(
			"FULL_MULTIBYTE",
			QrFamilyOptions::FULL_MULTIBYTE,
			"Enable Kanji/Hanzi compression for Latin-1 & binary data"
		);
	py::enum_<UltracodeOptions>(m, "UltracodeOptions", "Ultracode specific option (`symbol->option_3`)")
		.value("ULTRA_COMPRESSION", UltracodeOptions::ULTRA_COMPRESSION, "Enable Ultracode compression (experimental)");
	py::enum_<WarningLevel>(m, "WarningLevel", "Warning level (`symbol->warn_level`)")
		.value("DEFAULT", WarningLevel::DEFAULT, "Default behaviour")
		.value("FAIL_ALL", WarningLevel::FAIL_ALL, "Treat warning as error");
	py::enum_<CapabilityFlags>(m, "CapabilityFlags", "Capability flags (ZBarcode_Cap() `cap_flag`)")
		.value("HRT", CapabilityFlags::HRT, "Prints Human Readable Text?")
		.value("STACKABLE", CapabilityFlags::STACKABLE, "Is stackable?")
		.value("EANUPC", CapabilityFlags::EANUPC, "Is EAN/UPC?")
		.value("EXTENDABLE", CapabilityFlags::EXTENDABLE, "Legacy")
		.value("COMPOSITE", CapabilityFlags::COMPOSITE, "Can have composite data?")
		.value("ECI", CapabilityFlags::ECI, "Supports Extended Channel Interpretations?")
		.value("GS1", CapabilityFlags::GS1, "Supports GS1 data?")
		.value("DOTTY", CapabilityFlags::DOTTY, "Can be output as dots?")
		.value("QUIET_ZONES", CapabilityFlags::QUIET_ZONES, "Has default quiet zones?")
		.value("FIXED_RATIO", CapabilityFlags::FIXED_RATIO, "Has fixed width-to-height (aspect) ratio?")
		.value("READER_INIT", CapabilityFlags::READER_INIT, "Supports Reader Initialisation?")
		.value("FULL_MULTIBYTE", CapabilityFlags::FULL_MULTIBYTE, "Supports full-multibyte option?")
		.value("MASK", CapabilityFlags::MASK, "Is mask selectable?")
		.value("STRUCTAPP", CapabilityFlags::STRUCTAPP, "Supports Structured Append?")
		.value("COMPLIANT_HEIGHT", CapabilityFlags::COMPLIANT_HEIGHT, "Has compliant height?");
}
