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
    <link href="../../images/favicon2.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="../../css/narrative-print.css" media="print" rel="stylesheet" type="text/css" />
    <link href="../../css/narrative-screen.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="../../css/ancestortree.css" media="screen" rel="stylesheet" type="text/css" />
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
                    <li class = "CurrentSection"><a href="../../individuals.html" title="Individuals">Individuals</a></li>
                    <li><a href="../../index.html" title="Surnames">Surnames</a></li>
                    <li><a href="../../interactive_graph.html?indi={clean_pointer}" title="Interactive Graph">Interactive Graph</a></li>
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
                    {age_section}
                    <tr>
                        <td class="ColumnAttribute">Interactive Graph</td>
                        <td class="ColumnValue"><a href="../../interactive_graph.html?indi={clean_pointer}">View in Interactive Graph &rarr;</a></td>
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
                        </tr>
                    </thead>
                    <tbody>
{events_rows}
                    </tbody>
                </table>
            </div>
            {attributes_section}
            {parents_section}
            {families_section}
            {pedigree_section}
            {ancestors_section}
        </div>
        <div class="fullclear"></div>
        <div id="footer">
            <p id="createdate">
            Inspired by GRAMPS software.
            </p>
            <p id="copyright">

            </p>
        </div>
    </div>
</body>
</html>
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
    <td class="ColumnValue"><a href="../../{parent_path}">{parent_name}</a></td>
    <td class="ColumnDate">{parent_birth}</td>
    <td class="ColumnDate">{parent_death}</td>
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
        {spouse_html}
    </td>
</tr>
<tr>
    <td class="ColumnType">&nbsp;</td>
    <td class="ColumnAttribute">Children</td>
    <td class="ColumnValue">
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
    </td>
</tr>
"""

CHILD_ROW_TEMPLATE = """
<tr><td><a href="../../{child_path}">{child_name}</a></td><td>{child_birth}</td><td>{child_death}</td></tr>
"""

PEDIGREE_TEMPLATE = """
<div class="subsection" id="pedigree">
    <h4>Pedigree</h4>
    <ol class="pedigreegen">
        {pedigree_content}
    </ol>
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
        <script>
        function navFunction() {{ var x = document.getElementById("dropmenu"); if (x.className === "nav") {{ x.className += " responsive"; }} else {{ x.className = "nav"; }} }}
        function filterTable() {{
            var input = document.getElementById("searchInput");
            var clearBtn = document.getElementById("clearSearch");
            var filter = input.value.toLowerCase();
            var table = document.getElementById("dataTable");
            var rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
            var countSpan = document.getElementById("searchCount");
            var total = rows.length;
            var matches = 0;

            if (clearBtn) {{
                clearBtn.style.display = filter ? "inline" : "none";
            }}

            for (var i = 0; i < total; i++) {{
                var text = rows[i].textContent || rows[i].innerText;
                if (text.toLowerCase().indexOf(filter) > -1) {{
                    rows[i].style.display = "";
                    matches++;
                }} else {{
                    rows[i].style.display = "none";
                }}
            }}

            if (countSpan) {{
                if (filter) {{
                    countSpan.textContent = matches === 0 ? "No results found" : "Showing " + matches + " of " + total;
                }} else {{
                    countSpan.textContent = "";
                }}
            }}
        }}
        function clearSearchFilter() {{
            var input = document.getElementById("searchInput");
            if (input) {{
                input.value = "";
                filterTable();
                input.focus();
            }}
        }}
    </script>
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
            <div style="margin: 10px 0 15px 0; display: flex; align-items: center; gap: 8px;">
                <div style="position: relative; display: inline-block;">
                    <input type="text" id="searchInput" onkeyup="filterTable()" onkeydown="if(event.key === 'Escape') clearSearchFilter()" placeholder="Search surnames or given names..." style="padding: 6px 28px 6px 10px; width: 300px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;" />
                    <button id="clearSearch" type="button" onclick="clearSearchFilter()" style="display: none; position: absolute; right: 6px; top: 50%; transform: translateY(-50%); background: none; border: none; font-size: 16px; cursor: pointer; color: #888; padding: 0 4px;" title="Clear search">&times;</button>
                </div>
                <span id="searchCount" style="font-size: 13px; color: #666;"></span>
            </div>
            <table class="infolist" id="dataTable">
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
            Inspired by GRAMPS software.
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
        <script>
        function navFunction() {{ var x = document.getElementById("dropmenu"); if (x.className === "nav") {{ x.className += " responsive"; }} else {{ x.className = "nav"; }} }}
        function filterTable() {{
            var input = document.getElementById("searchInput");
            var clearBtn = document.getElementById("clearSearch");
            var filter = input.value.toLowerCase();
            var table = document.getElementById("dataTable");
            var rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
            var countSpan = document.getElementById("searchCount");
            var total = rows.length;
            var matches = 0;

            if (clearBtn) {{
                clearBtn.style.display = filter ? "inline" : "none";
            }}

            for (var i = 0; i < total; i++) {{
                var text = rows[i].textContent || rows[i].innerText;
                if (text.toLowerCase().indexOf(filter) > -1) {{
                    rows[i].style.display = "";
                    matches++;
                }} else {{
                    rows[i].style.display = "none";
                }}
            }}

            if (countSpan) {{
                if (filter) {{
                    countSpan.textContent = matches === 0 ? "No results found" : "Showing " + matches + " of " + total;
                }} else {{
                    countSpan.textContent = "";
                }}
            }}
        }}
        function clearSearchFilter() {{
            var input = document.getElementById("searchInput");
            if (input) {{
                input.value = "";
                filterTable();
                input.focus();
            }}
        }}
    </script>
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
            <div style="margin: 10px 0 15px 0; display: flex; align-items: center; gap: 8px;">
                <div style="position: relative; display: inline-block;">
                    <input type="text" id="searchInput" onkeyup="filterTable()" onkeydown="if(event.key === 'Escape') clearSearchFilter()" placeholder="Search individuals..." style="padding: 6px 28px 6px 10px; width: 300px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;" />
                    <button id="clearSearch" type="button" onclick="clearSearchFilter()" style="display: none; position: absolute; right: 6px; top: 50%; transform: translateY(-50%); background: none; border: none; font-size: 16px; cursor: pointer; color: #888; padding: 0 4px;" title="Clear search">&times;</button>
                </div>
                <span id="searchCount" style="font-size: 13px; color: #666;"></span>
            </div>
            <table class="infolist primobjlist" id="dataTable">
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
            Inspired by GRAMPS software.
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
    <script>
        function navFunction() {{ var x = document.getElementById("dropmenu"); if (x.className === "nav") {{ x.className += " responsive"; }} else {{ x.className = "nav"; }} }}
        function filterTable() {{
            var input = document.getElementById("searchInput");
            var clearBtn = document.getElementById("clearSearch");
            var filter = input.value.toLowerCase();
            var table = document.getElementById("dataTable");
            var rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
            var countSpan = document.getElementById("searchCount");
            var total = rows.length;
            var matches = 0;

            if (clearBtn) {{
                clearBtn.style.display = filter ? "inline" : "none";
            }}

            for (var i = 0; i < total; i++) {{
                var text = rows[i].textContent || rows[i].innerText;
                if (text.toLowerCase().indexOf(filter) > -1) {{
                    rows[i].style.display = "";
                    matches++;
                }} else {{
                    rows[i].style.display = "none";
                }}
            }}

            if (countSpan) {{
                if (filter) {{
                    countSpan.textContent = matches === 0 ? "No results found" : "Showing " + matches + " of " + total;
                }} else {{
                    countSpan.textContent = "";
                }}
            }}
        }}
        function clearSearchFilter() {{
            var input = document.getElementById("searchInput");
            if (input) {{
                input.value = "";
                filterTable();
                input.focus();
            }}
        }}
    </script>
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
            <div style="margin: 10px 0 15px 0; display: flex; align-items: center; gap: 8px;">
                <div style="position: relative; display: inline-block;">
                    <input type="text" id="searchInput" onkeyup="filterTable()" onkeydown="if(event.key === 'Escape') clearSearchFilter()" placeholder="Search individuals..." style="padding: 6px 28px 6px 10px; width: 300px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;" />
                    <button id="clearSearch" type="button" onclick="clearSearchFilter()" style="display: none; position: absolute; right: 6px; top: 50%; transform: translateY(-50%); background: none; border: none; font-size: 16px; cursor: pointer; color: #888; padding: 0 4px;" title="Clear search">&times;</button>
                </div>
                <span id="searchCount" style="font-size: 13px; color: #666;"></span>
            </div>
            <table class="infolist primobjlist surname" id="dataTable">
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
            Inspired by GRAMPS software.
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
                            <a href="../{path}">{given_name}</a>
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


ANCESTORS_TEMPLATE = """
<div class="subsection" id="ancestors">
    <h4>Ancestors</h4>
    <div class="tree-scroll-wrapper">
        {ancestors_content}
    </div>
</div>
"""

EVENT_ROW_TEMPLATE = """<tr>
    <td class="ColumnEvent">{event_name}</td>
    <td class="ColumnDate">{event_date}</td>
    <td class="ColumnPlace">{event_place}</td>
    <td class="ColumnDescription">{event_description}</td>
</tr>"""

ATTRIBUTES_SECTION_TEMPLATE = """<div class="subsection" id="attributes">
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
{attributes_rows}
        </tbody>
    </table>
</div>"""

ATTRIBUTE_ROW_TEMPLATE = """<tr>
    <td class="ColumnType">{attr_type}</td>
    <td class="ColumnValue">{attr_value}</td>
    <td class="ColumnNotes">{attr_notes}</td>
    <td class="ColumnSources">{attr_sources}</td>
</tr>"""
