stock_summary_xml = """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>MyReportStockSummaryForPeriod</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVFROMDATE>$fromDate$</SVFROMDATE>
                <SVTODATE>$toDate$</SVTODATE>
                <SVEXPORTFORMAT>ASCII (Comma Delimited)</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="MyReportStockSummaryForPeriod">
                        <FORMS>MyForm</FORMS>
                    </REPORT>
                    <FORM NAME="MyForm">
                        <PARTS>MyPart</PARTS>
                    </FORM>
                    <PART NAME="MyPart">
                        <LINES>MyLine</LINES>
                        <REPEAT>MyLine : MyCollection</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="MyLine">
                        <FIELDS>FldName</FIELDS>
                        <FIELDS>FldParent</FIELDS>
                        <FIELDS>FldOpeningQuantity</FIELDS>
                        <FIELDS>FldOpeningValue</FIELDS>
                        <FIELDS>FldInwardQuantity</FIELDS>
                        <FIELDS>FldInwardValue</FIELDS>
                        <FIELDS>FldOutwardQuantity</FIELDS>
                        <FIELDS>FldOutwardValue</FIELDS>
                        <FIELDS>FldClosingQuantity</FIELDS>
                        <FIELDS>FldClosingValue</FIELDS>
                    </LINE>
                    <FIELD NAME="FldName">
                        <SET>$$StringFindAndReplace:$Name:'"':'""'</SET>
                    </FIELD>
                    <FIELD NAME="FldParent">
                        <SET>$$StringFindAndReplace:$Parent:'"':'""'</SET>
                    </FIELD>
                    <FIELD NAME="FldOpeningQuantity">
                        <SET>if $$IsEmpty:$OpeningBalance then 0 else $$AsAmount:$OpeningBalance</SET>
                    </FIELD>
                    <FIELD NAME="FldOpeningValue">
                        <SET>if $$IsEmpty:$OpeningValue then 0 else $OpeningValue</SET>
                    </FIELD>
                    <FIELD NAME="FldInwardQuantity">
                        <SET>if $$IsEmpty:$InwardQuantity then 0 else $$AsAmount:$InwardQuantity</SET>
                    </FIELD>
                    <FIELD NAME="FldInwardValue">
                        <SET>if $$IsEmpty:$InwardValue then 0 else $InwardValue</SET>
                    </FIELD>
                    <FIELD NAME="FldOutwardQuantity">
                        <SET>if $$IsEmpty:$OutwardQuantity then 0 else $$AsAmount:$OutwardQuantity</SET>
                    </FIELD>
                    <FIELD NAME="FldOutwardValue">
                        <SET>if $$IsEmpty:$OutwardValue then 0 else $OutwardValue</SET>
                    </FIELD>
                    <FIELD NAME="FldClosingQuantity">
                        <SET>if $$IsEmpty:$ClosingBalance then 0 else $$AsAmount:$ClosingBalance</SET>
                    </FIELD>
                    <FIELD NAME="FldClosingValue">
                        <SET>if $$IsEmpty:$ClosingValue then 0 else $ClosingValue</SET>
                    </FIELD>
                    <COLLECTION NAME="MyCollection">
                        <TYPE>StockItem</TYPE>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""

stock_voucher_xml = """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
	<HEADER>
		<VERSION>1</VERSION>
		<TALLYREQUEST>Export</TALLYREQUEST>
		<TYPE>Data</TYPE>
		<ID>MyReportStockVoucherTable</ID>
	</HEADER>
	<BODY>
		<DESC>
			<STATICVARIABLES>
				<SVEXPORTFORMAT>XML (Data Interchange)</SVEXPORTFORMAT>
				<SVFROMDATE>$fromDate</SVFROMDATE>
				<SVTODATE>$toDate</SVTODATE>
				<SVCURRENTCOMPANY>$targetCompany</SVCURRENTCOMPANY>
			</STATICVARIABLES>
			<TDL>
				<TDLMESSAGE>
					<REPORT NAME="MyReportStockVoucherTable">
						<FORMS>MyForm</FORMS>
					</REPORT>
					<FORM NAME="MyForm">
						<PARTS>MyPart01</PARTS>
						<XMLTAG>DATA</XMLTAG>
					</FORM>
					<PART NAME="MyPart01">
						<LINES>MyLine01</LINES>
						<REPEAT>MyLine01 : MyCollection</REPEAT>
						<SCROLLED>Vertical</SCROLLED>
					</PART>
					<PART NAME="MyPart02">
						<LINES>MyLine02</LINES>
						<REPEAT>MyLine02 : AllInventoryEntries</REPEAT>
						<SCROLLED>Vertical</SCROLLED>
					</PART>
					<LINE NAME="MyLine01">
						<FIELDS>FldDate,FldVoucherType,FldVoucherNumber,FldPartyName,FldVoucherCategory,FldNarration</FIELDS>
						<EXPLODE>MyPart02</EXPLODE>
						<XMLTAG>VOUCHER</XMLTAG>
					</LINE>
					<LINE NAME="MyLine02">
						<FIELDS>FldStockItemName,FldStockQuantity,FldStockAmount,FldStockGodown</FIELDS>
						<XMLTAG>INVENTORY_ALLOCATION</XMLTAG>
					</LINE>
					<FIELD NAME="FldDate">
						<SET>$Date</SET>
						<XMLTAG>DATE</XMLTAG>
					</FIELD>
					<FIELD NAME="FldVoucherType">
						<SET>$VoucherTypeName</SET>
						<XMLTAG>VOUCHERTYPE</XMLTAG>
					</FIELD>
					<FIELD NAME="FldVoucherNumber">
						<SET>if $$IsEmpty:$VoucherNumber then $$StrByCharCode:245 else $VoucherNumber</SET>
						<XMLTAG>VOUCHERNUMBER</XMLTAG>
					</FIELD>
					<FIELD NAME="FldPartyName">
						<SET>if $$IsEmpty:$PartyLedgerName then $$StrByCharCode:245 else $PartyLedgerName</SET>
						<XMLTAG>PARTYNAME</XMLTAG>
					</FIELD>
					<FIELD NAME="FldVoucherCategory">
						<SET>$Parent:VoucherType:$VoucherTypeName</SET>
						<XMLTAG>VOUCHERCATEGORY</XMLTAG>
					</FIELD>
					<FIELD NAME="FldNarration">
						<SET>if $$IsEmpty:$Narration then $$StrByCharCode:245 else $Narration</SET>
						<XMLTAG>Narration</XMLTAG>
					</FIELD>
					<FIELD NAME="FldStockItemName">
						<SET>$StockItemName</SET>
						<XMLTAG>STOCKITEM</XMLTAG>
					</FIELD>
					<FIELD NAME="FldStockQuantity">
						<SET>$$StringFindAndReplace:(if $$IsInwards:$BilledQty then $$Number:$$String:$BilledQty:"TailUnits" else -$$Number:$$String:$BilledQty:"TailUnits"):"(-)":"-"</SET>
						<XMLTAG>QUANTITY</XMLTAG>
					</FIELD>
					<FIELD NAME="FldStockAmount">
						<SET>$$StringFindAndReplace:(if $$IsDebit:$Amount then -$$NumValue:$Amount else $$NumValue:$Amount):"(-)":"-"</SET>
						<XMLTAG>AMOUNT</XMLTAG>
					</FIELD>
					<FIELD NAME="FldStockGodown">
						<SET>$GodownName</SET>
						<XMLTAG>GODOWN</XMLTAG>
					</FIELD>
					<COLLECTION NAME="MyCollection">
						<TYPE>Voucher</TYPE>
						<FETCH>AllInventoryEntries</FETCH>
						<FETCH>Narration</FETCH>
						<FETCH>PartyLedgerName</FETCH>
						<FETCH>EmptyInventory</FETCH>
						<FILTER>Fltr01,Fltr02</FILTER>
					</COLLECTION>
					<SYSTEM TYPE="Formulae" NAME="Fltr01">NOT $IsCancelled</SYSTEM>
					<SYSTEM TYPE="Formulae" NAME="Fltr02">NOT $IsOptional</SYSTEM>
				</TDLMESSAGE>
			</TDL>
		</DESC>
	</BODY>
</ENVELOPE>
"""


account_voucher_view_xml="""
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
	<HEADER>
		<VERSION>1</VERSION>
		<TALLYREQUEST>Export</TALLYREQUEST>
		<TYPE>Data</TYPE>
		<ID>MyReportAccountingVoucherTable</ID>
	</HEADER>
	<BODY>
		<DESC>
			<STATICVARIABLES>
				<SVEXPORTFORMAT>XML (Data Interchange)</SVEXPORTFORMAT>
                <SVFROMDATE>$fromDate</SVFROMDATE>
				<SVTODATE>$toDate</SVTODATE>
                <SVCURRENTCOMPANY>$targetCompany</SVCURRENTCOMPANY>
			</STATICVARIABLES>
			<TDL>
				<TDLMESSAGE>
					<REPORT NAME="MyReportAccountingVoucherTable">
						<FORMS>MyForm</FORMS>
					</REPORT>
					<FORM NAME="MyForm">
						<PARTS>MyPart01</PARTS>
                        <XMLTAG>DATA</XMLTAG>
					</FORM>
					<PART NAME="MyPart01">
						<LINES>MyLine01</LINES>
						<REPEAT>MyLine01 : MyCollection</REPEAT>
						<SCROLLED>Vertical</SCROLLED>
					</PART>
					<PART NAME="MyPart02">
						<LINES>MyLine02</LINES>
						<REPEAT>MyLine02 : AllLedgerEntries</REPEAT>
						<SCROLLED>Vertical</SCROLLED>
					</PART>
					<LINE NAME="MyLine01">
                        <FIELDS>FldDate,FldVoucherType,FldVoucherNumber,FldPartyName,FldVoucherCategory,FldNarration</FIELDS>
						<EXPLODE>MyPart02</EXPLODE>
                        <XMLTAG>VOUCHER</XMLTAG>
					</LINE>
					<LINE NAME="MyLine02">
						<FIELDS>FldLedgerName,FldLedgerAmount</FIELDS>
                        <XMLTAG>ACCOUNTING_ALLOCATION</XMLTAG>
					</LINE>
					<FIELD NAME="FldDate">
						<SET>$Date</SET>
						<XMLTAG>DATE</XMLTAG>
					</FIELD>
                    <FIELD NAME="FldVoucherType">
						<SET>$VoucherTypeName</SET>
						<XMLTAG>VOUCHERTYPE</XMLTAG>
					</FIELD>
                    <FIELD NAME="FldVoucherNumber">
						<SET>if $$IsEmpty:$VoucherNumber then $$StrByCharCode:245 else $VoucherNumber</SET>
						<XMLTAG>VOUCHERNUMBER</XMLTAG>
					</FIELD>
                    <FIELD NAME="FldPartyName">
						<SET>if $$IsEmpty:$PartyLedgerName then $$StrByCharCode:245 else $PartyLedgerName</SET>
						<XMLTAG>PARTYNAME</XMLTAG>
					</FIELD>
                    <FIELD NAME="FldVoucherCategory">
						<SET>$Parent:VoucherType:$VoucherTypeName</SET>
						<XMLTAG>VOUCHERCATEGORY</XMLTAG>
					</FIELD>
                    <FIELD NAME="FldNarration">
						<SET>if $$IsEmpty:$Narration then $$StrByCharCode:245 else $Narration</SET>
						<XMLTAG>Narration</XMLTAG>
					</FIELD>
					<FIELD NAME="FldLedgerName">
						<SET>$LedgerName</SET>
						<XMLTAG>LEDGER</XMLTAG>
					</FIELD>
					<FIELD NAME="FldLedgerAmount">
						<SET>$$StringFindAndReplace:(if $$IsDebit:$Amount then -$$NumValue:$Amount else $$NumValue:$Amount):"(-)":"-"</SET>
						<XMLTAG>AMOUNT</XMLTAG>
					</FIELD>
					<COLLECTION NAME="MyCollection">
						<TYPE>Voucher</TYPE>
						<FETCH>AllLedgerEntries</FETCH>
                        <FETCH>Narration</FETCH>
                        <FETCH>PartyLedgerName</FETCH>
						<FILTER>Fltr01,Fltr02</FILTER>
					</COLLECTION>
					<SYSTEM TYPE="Formulae" NAME="Fltr01">NOT $IsCancelled</SYSTEM>
					<SYSTEM TYPE="Formulae" NAME="Fltr02">NOT $IsOptional</SYSTEM>
				</TDLMESSAGE>
			</TDL>
		</DESC>
	</BODY>
</ENVELOPE>"""

closing_stock_values_xml = """
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>MyReportLedgerTable</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>ASCII (Comma Delimited)</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="MyReportLedgerTable">
                        <FORMS>MyForm</FORMS>
                    </REPORT>
                    <FORM NAME="MyForm">
                        <PARTS>MyPart</PARTS>
                    </FORM>
                    <PART NAME="MyPart">
                        <LINES>MyLine</LINES>
                        <REPEAT>MyLine : MyCollection</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <PART NAME="MyClosingValuesPart">
                        <LINES>MyClosingValuesLine</LINES>
                        <REPEAT>MyClosingValuesLine : LedgerClosingValues</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="MyLine">
                        <FIELDS>FldBlank</FIELDS>
                        <EXPLODE>MyClosingValuesPart</EXPLODE>
                    </LINE>
                    <LINE NAME="MyClosingValuesLine">
                        <FIELDS>FldGuid,FldName,FldParent,FldClosingDate,FldClosingValue</FIELDS>
                    </LINE>
                    <FIELD NAME="FldBlank">
                        <SET>""</SET>
                    </FIELD>
                    <FIELD NAME="FldGuid">
                        <SET>$Guid</SET>
                    </FIELD>
                    <FIELD NAME="FldName">
                        <SET>$$StringFindAndReplace:$Name:'"':'""'</SET>
                    </FIELD>
                    <FIELD NAME="FldParent">
                        <SET>$$StringFindAndReplace:$Parent:'"':'""'</SET>
                    </FIELD>
                    <FIELD NAME="FldClosingDate">
                        <SET>$Date</SET>
                    </FIELD>
                    <FIELD NAME="FldClosingValue">
                        <SET>if $$IsEmpty:$Amount then 0 else $Amount</SET>
                    </FIELD>
                    <COLLECTION NAME="MyCollection">
                        <TYPE>Ledger</TYPE>
                        <FETCH>LedgerClosingValues</FETCH>
                        <FILTER>FilterLedger</FILTER>
                    </COLLECTION>
                    <SYSTEM TYPE="Formulae" NAME="FilterLedger">$$IsLedOfGrp:$Name:$$GroupStock</SYSTEM>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>
"""
balance_sheet_xml = """<ENVELOPE>
<HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
<BODY>
    <EXPORTDATA>
        <REQUESTDESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <REPORTNAME>Balance Sheet</REPORTNAME>
        </REQUESTDESC>
    </EXPORTDATA>
</BODY>
</ENVELOPE>"""

group_table_xml = """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>MyReportGroupTable</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>ASCII (Comma Delimited)</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="MyReportGroupTable">
                        <FORMS>MyForm</FORMS>
                    </REPORT>
                    <FORM NAME="MyForm">
                        <PARTS>MyPart</PARTS>
                    </FORM>
                    <PART NAME="MyPart">
                        <LINES>MyLine</LINES>
                        <REPEAT>MyLine : MyCollection</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="MyLine">
                        <FIELDS>FldGuid,FldName,FldParent,FldPrimaryGroup,FldIsRevenue,FldIsDeemedPositive,FldAffectsGrossProfit,FldSortPosition</FIELDS>
                    </LINE>
                    <FIELD NAME="FldGuid">
                        <SET>$Guid</SET>
                    </FIELD>
                    <FIELD NAME="FldName">
                        <SET>$$StringFindAndReplace:$Name:'"':'""'</SET>
                    </FIELD>
                    <FIELD NAME="FldParent">
                        <SET>$$StringFindAndReplace:$Parent:'"':'""'</SET>
                    </FIELD>
                    <FIELD NAME="FldPrimaryGroup">
                        <SET>$$StringFindAndReplace:$PrimaryGroup:'"':'""'</SET>
                    </FIELD>
                    <FIELD NAME="FldIsRevenue">
                        <SET>$IsRevenue</SET>
                    </FIELD>
                    <FIELD NAME="FldIsDeemedPositive">
                        <SET>$IsDeemedPositive</SET>
                    </FIELD>
                    <FIELD NAME="FldAffectsGrossProfit">
                        <SET>$AffectsGrossProfit</SET>
                    </FIELD>
                    <FIELD NAME="FldSortPosition">
                        <SET>$SortPosition</SET>
                    </FIELD>
                    <COLLECTION NAME="MyCollection">
                        <TYPE>Group</TYPE>
                        <FETCH>IsRevenue,AffectsGrossProfit,IsDeemedPositive,SortPosition,PrimaryGroup</FETCH>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""

bills_payable_xml = """<ENVELOPE>
<HEADER>
<TALLYREQUEST>Export Data</TALLYREQUEST>
</HEADER>
<BODY>
<EXPORTDATA>
<REQUESTDESC>
<STATICVARIABLES>
<!-- Specify the period here -->
<SVFROMDATE>20240401</SVFROMDATE>
<SVTODATE>20260331</SVTODATE>
<!-- Specify the Export format here  HTML or XML or SDF -->
<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
</STATICVARIABLES>
<!-- Specify the Report Name here -->
<REPORTNAME>Bills Payable</REPORTNAME>
</REQUESTDESC>
</EXPORTDATA>
</BODY>
</ENVELOPE>"""

bills_receivable_xml = """<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>BillsReceivable</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>XML (Data Interchange)</SVEXPORTFORMAT>
                <SVFROMDATE>20240401</SVFROMDATE>
                <SVTODATE>20260331</SVTODATE>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="Bills Receivable">
                        <FORMS>MyForm</FORMS>
                    </REPORT>
                    <FORM NAME="MyForm">
                        <PARTS>MyPart</PARTS>
                    </FORM>
                    <PART NAME="MyPart">
                        <LINES>MyLine</LINES>
                        <REPEAT>MyLine : MyCollection</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="MyLine">
                        <FIELDS>FldBillRef,FldBillDate,FldDueDate,FldAmount,FldParty,FldOverdue</FIELDS>
                    </LINE>
                    <FIELD NAME="FldBillRef">
                        <SET>$BillRef</SET>
                    </FIELD>
                    <FIELD NAME="FldBillDate">
                        <SET>$BillDate</SET>
                    </FIELD>
                    <FIELD NAME="FldDueDate">
                        <SET>$DueDate</SET>
                    </FIELD>
                    <FIELD NAME="FldAmount">
                        <SET>$Amount</SET>
                    </FIELD>
                    <FIELD NAME="FldParty">
                        <SET>$Party</SET>
                    </FIELD>
                    <FIELD NAME="FldOverdue">
                        <SET>$Overdue</SET>
                    </FIELD>
                    <COLLECTION NAME="MyCollection">
                        <TYPE>Bill</TYPE>
                        <FETCH>BillRef,BillDate,DueDate,Amount,Party,Overdue</FETCH>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""