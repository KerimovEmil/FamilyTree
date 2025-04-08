#!/usr/bin/env python3
"""
Constants and templates for generating HTML files from GEDCOM data.
"""

# File paths
GEDCOM_FILE = 'ged/family_tree.ged'
OUTPUT_DIR = 'ppl'
SURNAMES_DIR = 'surnames'

# HTML Templates
HTML_TEMPLATE = """<!DOCTYPE html>
<html xml:lang="en-GB" lang="en-GB" xmlns="http://www.w3.org/1999/xhtml">
<head lang="en-GB">
    <title>My Family Tree - {name}</title>
    <meta charset="UTF-8" />
    <meta name ="viewport" content="width=device-width; height=device-height; initial-scale=1.0; minimum-scale=0.5; maximum-scale=10.0; user-scalable=yes" />
    <meta name ="apple-mobile-web-app-capable" content="yes" />
    <meta name="author" content="" />
    <link href="../../../images/favicon2.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="../../../css/narrative-print.css" media="print" rel="stylesheet" type="text/css" />
    <link href="../../../css/narrative-screen.css" media="screen" rel="stylesheet" type="text/css" />
    <script>function navFunction() {{ var x = document.getElementById("dropmenu"); if (x.className === "nav") {{ x.className += " responsive"; }} else {{ x.className = "nav"; }} }}</script>
    <link href="../../../css/ancestortree.css" media="screen" rel="stylesheet" type="text/css" />
</head>
<body>
    <div id="outerwrapper">
        <div id="header">
            <a href="javascript:void(0);" class="navIcon" onclick="navFunction()">&#8801;</a>
            <h1 id="SiteTitle">My Family Tree</h1>
        </div>
        <div class="wrappernav" id="nav" role="navigation">
            <div class="container">
                <ul class="nav" id="dropmenu">
                    <li class = "CurrentSection"><a href="../../../individuals.html" title="Individuals">Individuals</a></li>
                    <li><a href="../../../index.html" title="Surnames">Surnames</a></li>
                    <li><a href="../../../interactive_graph.html" title="Interactive Graph">Interactive Graph</a></li>
                </ul>
            </div>
        </div>
        <div class="content" id="IndividualDetail">
            <h3>{name}<sup><small></small></sup></h3>
            <div id="summaryarea">
                <table class="infolist">
                    <tr>
                        <td class="ColumnAttribute">Birth Name</td>
                        <td class="ColumnValue">
                        {name}
                        </td>
                    </tr>
                    {married_name_section}
                    <tr>
                        <td class="ColumnAttribute">Gender</td>
                        <td class="ColumnValue">{gender}</td>
                    </tr>
                </table>
            </div>
            <div class="subsection" id="events">
                <h4>Events</h4>
                <table class="infolist eventlist">
                    <thead>
                        <tr>
                            <th class="ColumnEvent">Event</th>
                            <th class="ColumnDate">Date</th>
                            <th class="ColumnPlace">Place</th>
                            <th class="ColumnDescription">Description</th>
                            <th class="ColumnSources">Sources</th>
                            </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="ColumnEvent">
                            Birth
                            </td>
                            <td class="ColumnDate">{birth_date}</td>
                            <td class="ColumnPlace">
                                {birth_place}
                            </td>
                            <td class="ColumnDescription">&nbsp;</td>
                            <td class="ColumnSources" rowspan="2">
                            &nbsp;
                            </td>
                            <tr>
                                <td class="ColumnEvent">

                                </td>
                                <td class="ColumnNotes" colspan="3">
                                    <div>
                                    </div>
                                </td>
                            </tr>
                        </tr>
                        {death_section}
                        {occupation_section}
                    </tbody>
                </table>
            </div>
            {parents_section}
            {families_section}
            <div class="subsection" id="attributes">
                <h4>Attributes</h4>
                <table class="infolist attrlist">
                    <thead>
                        <tr>
                            <th class="ColumnType">Type</th>
                            <th class="ColumnValue">Value</th>
                            <th class="ColumnNotes">Notes</th>
                            <th class="ColumnSources">Sources</th>
                        </tr>
                    </thead>
                    <tbody>
                        {attributes_section}
                    </tbody>
                </table>
            </div>
            {pedigree_section}
            {ancestors_section}
        </div>
        <div class="fullclear"></div>
        <div id="footer">
            <p id="createdate">
            Generated on {current_date}
            </p>
            <p id="copyright">

            </p>
        </div>
    </div>
</body>
</html>
"""

OCCUPATION_TEMPLATE = """
<tr>
    <td class="ColumnEvent">
    Occupation
    </td>
    <td class="ColumnDate">&nbsp;</td>
    <td class="ColumnPlace">&nbsp;</td>
    <td class="ColumnDescription">{occupation}</td>
    <td class="ColumnSources" rowspan="2">
    &nbsp;
    </td>
    <tr>
        <td class="ColumnEvent">

        </td>
        <td class="ColumnNotes" colspan="3">
            <div>
            </div>
        </td>
    </tr>
</tr>
"""

DEATH_TEMPLATE = """
<tr>
    <td class="ColumnEvent">
    Death
    </td>
    <td class="ColumnDate">{death_date}</td>
    <td class="ColumnPlace">
        {death_place}
    </td>
    <td class="ColumnDescription">&nbsp;</td>
    <td class="ColumnSources" rowspan="2">
    &nbsp;
    </td>
    <tr>
        <td class="ColumnEvent">

        </td>
        <td class="ColumnNotes" colspan="3">
            <div>
            </div>
        </td>
    </tr>
</tr>
"""

MARRIED_NAME_TEMPLATE = """
<tr>
    <td class="ColumnAttribute">Married Name</td>
    <td class="ColumnValue">
    {married_name}
    </td>
</tr>
"""

PARENTS_TEMPLATE = """
<div class="subsection" id="parents">
    <h4>Parents</h4>
    <table class="infolist">
        <thead>
            <tr>
                <th class="ColumnAttribute">Relation to main person</th>
                <th class="ColumnValue">Name</th>
                <th class="ColumnValue">Birth date</th>
                <th class="ColumnValue">Death date</th>
                <th class="ColumnValue">Relation within this family (if not by birth)</th>
            </tr>
        </thead>
        <tbody>
            {parents_rows}
        </tbody>
    </table>
</div>
"""

PARENT_ROW_TEMPLATE = """
<tr>
    <td class="ColumnAttribute">{relation}</td>
    <td class="ColumnValue" /><a href="../../../{parent_path}">{parent_name}</a><td class="ColumnDate" />{parent_birth}<td class="ColumnDate" />{parent_death}
</tr>
"""

SIBLING_ROW_TEMPLATE = """
<tr>
    <td class="ColumnAttribute">&nbsp;&nbsp;&nbsp;&nbsp;{relation}</td>
    <td class="ColumnValue">&nbsp;&nbsp;&nbsp;&nbsp;{sibling_link}</td>
    <td class="ColumnDate">{sibling_birth}</td>
    <td class="ColumnDate">{sibling_death}</td>
    <td class="ColumnValue"></td>
</tr>
"""

FAMILIES_TEMPLATE = """
<div class="subsection" id="families">
    <h4>Families</h4>
    <table class="infolist">
        {families_rows}
    </table>
</div>
"""

FAMILY_ROW_TEMPLATE = """
<tr class="BeginFamily">
    <td class="ColumnValue" colspan="3"><H4 class="subsection"><a href="" title="Family of {husband_name} and {wife_name}">Family of {husband_name} and {wife_name}</a></H4></td>
</tr>
<tr class="BeginFamily">
    <td class="ColumnType">Married</td>
    <td class="ColumnAttribute">{spouse_relation}</td>
    <td class="ColumnValue">
        <a href="../../../{spouse_path}">{spouse_name}</a>
     ( *
    {spouse_birth}
     +
    {spouse_death}
     )
    </td>
</tr>
<tr>
    <td class="ColumnType">&nbsp;</td>
    <td class="ColumnAttribute">Children</td>
    <td class="ColumnValue" />
    <table class="infolist eventlist">
        <thead>
            <tr>
                <th class="ColumnName">Name</th>
                <th class="ColumnDate">Birth Date</th>
                <th class="ColumnDate">Death Date</th>
            </tr>
        </thead>
        <tbody>
            {children_rows}
        </tbody>
    </table>
</tr>
"""

CHILD_ROW_TEMPLATE = """
<tr><td /><a href="../../../{child_path}">{child_name}</a><td>{child_birth}</td><td>{child_death}</td></tr>
"""

PEDIGREE_TEMPLATE = """
<div class="subsection" id="pedigree">
    <h4>Pedigree</h4>
    <ol class="pedigreegen">
        {pedigree_content}
    </ol>
</div>
"""

ANCESTORS_TEMPLATE = """
<div class="subsection" id="tree">
    <h4>Ancestors</h4>
    {ancestors_content}
</div>
"""

# Index and individuals page templates
INDEX_HTML_TEMPLATE = """<!DOCTYPE html>
<html xml:lang="en-GB" lang="en-GB" xmlns="http://www.w3.org/1999/xhtml">
<head lang="en-GB">
    <title>My Family Tree - Surnames</title>
    <meta charset="UTF-8" />
    <meta name ="viewport" content="width=device-width; height=device-height; initial-scale=1.0; minimum-scale=0.5; maximum-scale=10.0; user-scalable=yes" />
    <meta name ="apple-mobile-web-app-capable" content="yes" />
    <meta name="author" content="" />
    <link href="images/favicon2.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="css/narrative-print.css" media="print" rel="stylesheet" type="text/css" />
    <link href="css/narrative-screen.css" media="screen" rel="stylesheet" type="text/css" />
    <script>function navFunction() {{ var x = document.getElementById("dropmenu"); if (x.className === "nav") {{ x.className += " responsive"; }} else {{ x.className = "nav"; }} }}</script>
</head>
<body>
    <div id="outerwrapper">
        <div id="header">
            <a href="javascript:void(0);" class="navIcon" onclick="navFunction()">&#8801;</a>
            <h1 id="SiteTitle">My Family Tree</h1>
        </div>
        <div class="wrappernav" id="nav" role="navigation">
            <div class="container">
                <ul class="nav" id="dropmenu">
                    <li><a href="individuals.html" title="Individuals">Individuals</a></li>
                    <li class="CurrentSection"><a href="index.html" title="Surnames">Surnames</a></li>
                    <li><a href="interactive_graph.html" title="Interactive Graph">Interactive Graph</a></li>
                </ul>
            </div>
        </div>
        <div class="content" id="SurnameDetail">
            <h3>Surnames</h3>
            <p>This page contains an index of all the surnames in the database. Selecting a name will lead to a page for that surname.</p>
            <table class="infolist">
                <thead>
                    <tr>
                        <th class="ColumnSurname">Surname</th>
                        <th class="ColumnName">Given Name</th>
                    </tr>
                </thead>
                <tbody>
{surname_entries}
                </tbody>
            </table>
        </div>
        <div class="fullclear"></div>
        <div id="footer">
            <p id="createdate">
            Generated on {current_date}
            </p>
            <p id="copyright">
            </p>
        </div>
    </div>
</body>
</html>
"""

INDIVIDUALS_HTML_TEMPLATE = """<!DOCTYPE html>
<html xml:lang="en-GB" lang="en-GB" xmlns="http://www.w3.org/1999/xhtml">
<head lang="en-GB">
    <title>My Family Tree - Individuals</title>
    <meta charset="UTF-8" />
    <meta name ="viewport" content="width=device-width; height=device-height; initial-scale=1.0; minimum-scale=0.5; maximum-scale=10.0; user-scalable=yes" />
    <meta name ="apple-mobile-web-app-capable" content="yes" />
    <meta name="author" content="" />
    <link href="images/favicon2.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="css/narrative-print.css" media="print" rel="stylesheet" type="text/css" />
    <link href="css/narrative-screen.css" media="screen" rel="stylesheet" type="text/css" />
    <script>function navFunction() {{ var x = document.getElementById("dropmenu"); if (x.className === "nav") {{ x.className += " responsive"; }} else {{ x.className = "nav"; }} }}</script>
</head>
<body>
    <div id="outerwrapper">
        <div id="header">
            <a href="javascript:void(0);" class="navIcon" onclick="navFunction()">&#8801;</a>
            <h1 id="SiteTitle">My Family Tree</h1>
        </div>
        <div class="wrappernav" id="nav" role="navigation">
            <div class="container">
                <ul class="nav" id="dropmenu">
                    <li class="CurrentSection"><a href="individuals.html" title="Individuals">Individuals</a></li>
                    <li><a href="index.html" title="Surnames">Surnames</a></li>
                    <li><a href="interactive_graph.html" title="Interactive Graph">Interactive Graph</a></li>
                </ul>
            </div>
        </div>
        <div class="content" id="IndividualList">
            <h3>Individuals</h3>
            <table class="infolist primobjlist">
                <thead>
                    <tr>
                        <th class="ColumnName">Name</th>
                        <th class="ColumnDate">Birth</th>
                        <th class="ColumnDate">Death</th>
                    </tr>
                </thead>
                <tbody>
{individual_entries}
                </tbody>
            </table>
        </div>
        <div class="fullclear"></div>
        <div id="footer">
            <p id="createdate">
            Generated on {current_date}
            </p>
            <p id="copyright">
            </p>
        </div>
    </div>
</body>
</html>
"""

SURNAME_ENTRY_TEMPLATE = """                    <tr>
                        <td class="ColumnSurname"><a href="{surname_path}" title="{surname}">{surname}</a></td>
                        <td class="ColumnName">
{given_names}</td>
                    </tr>
"""

SURNAME_PAGE_TEMPLATE = """<!DOCTYPE html>
<html xml:lang="en-GB" lang="en-GB" xmlns="http://www.w3.org/1999/xhtml">
<head lang="en-GB">
    <title>My Family Tree - Surname - {surname}</title>
    <meta charset="UTF-8" />
    <meta name ="viewport" content="width=device-width; height=device-height; initial-scale=1.0; minimum-scale=0.5; maximum-scale=10.0; user-scalable=yes" />
    <meta name ="apple-mobile-web-app-capable" content="yes" />
    <meta name="author" content="" />
    <link href="../images/favicon2.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="../css/narrative-print.css" media="print" rel="stylesheet" type="text/css" />
    <link href="../css/narrative-screen.css" media="screen" rel="stylesheet" type="text/css" />
    <script>function navFunction() {{ var x = document.getElementById("dropmenu"); if (x.className === "nav") {{ x.className += " responsive"; }} else {{ x.className = "nav"; }} }}</script>
</head>
<body>
    <div id="outerwrapper">
        <div id="header">
            <a href="javascript:void(0);" class="navIcon" onclick="navFunction()">&#8801;</a>
            <h1 id="SiteTitle">My Family Tree</h1>
        </div>
        <div class="wrappernav" id="nav" role="navigation">
            <div class="container">
                <ul class="nav" id="dropmenu">
                    <li><a href="../individuals.html" title="Individuals">Individuals</a></li>
                    <li class="CurrentSection"><a href="../index.html" title="Surnames">Surnames</a></li>
                    <li><a href="../interactive_graph.html" title="Interactive Graph">Interactive Graph</a></li>
                </ul>
            </div>
        </div>
        <div class="content" id="SurnameDetail">
            <h3>{surname}</h3>
            <p id="description">
            This page contains an index of all the individuals in the database with the surname of {surname}. Selecting the person&#8217;s name will take you to that person&#8217;s individual page.
            </p>
            <table class="infolist primobjlist surname">
                <thead>
                    <tr>
                        <th class="ColumnName">Name</th>
                        <th class="ColumnDate">Birth</th>
                    </tr>
                </thead>
                <tbody>
{individual_entries}
                </tbody>
            </table>
        </div>
        <div class="fullclear"></div>
        <div id="footer">
            <p id="createdate">
            Generated on {current_date}
            </p>
            <p id="copyright">
            </p>
        </div>
    </div>
</body>
</html>
"""

SURNAME_INDIVIDUAL_ENTRY_TEMPLATE = """                    <tr>
                        <td class="ColumnName">
                            <a href="{individual_path}">{individual_name}</a>
                        </td>
                        <td class="ColumnBirth">{birth_date}</td>
                    </tr>
"""

INDIVIDUAL_ENTRY_TEMPLATE = """                    <tr>
                        <td class="ColumnName"><a href="{path}" title="{name}">{name}</a></td>
                        <td class="ColumnDate">{birth_date}</td>
                        <td class="ColumnDate">{death_date}</td>
                    </tr>
"""
