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
                    <li><a href="../../relationship.html?p1={clean_pointer}" title="Relationship Finder">Relationship</a></li>
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
                    {alt_names_section}
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
                    <tr>
                        <td class="ColumnAttribute">Relationship</td>
                        <td class="ColumnValue"><a href="../../relationship.html?p1={clean_pointer}">Find relationship with... &rarr;</a></td>
                    </tr>
                </table>
                {photo_section}
            </div>
            {notes_section}
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
                    <li><a href="relationship.html" title="Relationship Finder">Relationship</a></li>
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
                    <li><a href="relationship.html" title="Relationship Finder">Relationship</a></li>
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
                    <li><a href="../relationship.html" title="Relationship Finder">Relationship</a></li>
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

NOTES_SECTION_TEMPLATE = """<div class="subsection" id="notes">
    <h4>Notes &amp; Biography</h4>
    <div class="grampsstylednote" style="background: #f9fbfd; border-left: 4px solid #2b6cb0; padding: 12px 16px; border-radius: 4px; margin: 8px 0 16px 0; line-height: 1.6;">
        {notes_items}
    </div>
</div>"""

PHOTO_SECTION_TEMPLATE = """<div class="individual-photos" style="margin: 12px 0;">
    {photo_items}
</div>"""


RELATIONSHIP_FINDER_TEMPLATE = """<!DOCTYPE html>
<html xml:lang="en-GB" lang="en-GB" xmlns="http://www.w3.org/1999/xhtml">
<head lang="en-GB">
    <title>My Family Tree - Relationship Finder</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width; height=device-height; initial-scale=1.0; minimum-scale=0.5; maximum-scale=10.0; user-scalable=yes" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="author" content="" />
    <link href="images/favicon2.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="css/narrative-print.css" media="print" rel="stylesheet" type="text/css" />
    <link href="css/narrative-screen.css" media="screen" rel="stylesheet" type="text/css" />
    <style>
        .rel-controls {{
            display: flex;
            flex-wrap: wrap;
            align-items: flex-end;
            gap: 12px;
            margin: 20px 0 25px 0;
            background: #f9f9f9;
            padding: 16px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }}
        .rel-field {{
            flex: 1 1 280px;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        .rel-field label {{
            font-weight: bold;
            font-size: 13px;
            color: #333;
        }}
        .rel-field input {{
            padding: 8px 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
        }}
        .rel-btn {{
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 4px;
            cursor: pointer;
            border: 1px solid #aaa;
            background: #f0f0f0;
            font-weight: 500;
        }}
        .rel-btn:hover {{
            background: #e4e4e4;
        }}
        .rel-btn-primary {{
            background: #2b6cb0;
            color: #fff;
            border-color: #2b6cb0;
        }}
        .rel-btn-primary:hover {{
            background: #205081;
        }}
        #swapBtn {{
            font-size: 18px;
            padding: 6px 12px;
            align-self: flex-end;
            margin-bottom: 2px;
        }}
        .rel-summary-box {{
            background: #edf2f7;
            border-left: 4px solid #3182ce;
            padding: 14px 18px;
            border-radius: 4px;
            margin-bottom: 25px;
        }}
        .rel-headline {{
            font-size: 18px;
            font-weight: bold;
            color: #2b6cb0;
            margin: 0 0 6px 0;
        }}
        .rel-meta {{
            font-size: 13px;
            color: #555;
            margin: 0;
        }}
        .chain-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 600px;
            margin: 0 auto 30px auto;
        }}
        .person-card {{
            display: block;
            text-decoration: none;
            width: 100%;
            box-sizing: border-box;
            background: #ffffff;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            padding: 12px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: transform 0.15s, box-shadow 0.15s;
            position: relative;
        }}
        .person-card:hover {{
            transform: translateY(-1px);
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }}
        .person-card.male {{
            border-left: 5px solid #4299e1;
            background: #fbfdff;
        }}
        .person-card.female {{
            border-left: 5px solid #ed64a6;
            background: #fffbfe;
        }}
        .person-card.common-ancestor {{
            border: 2px solid #ecc94b;
            border-left: 6px solid #d69e2e;
            background: #fffff0;
        }}
        .card-name {{
            font-size: 15px;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 3px;
        }}
        .card-dates {{
            font-size: 12px;
            color: #718096;
        }}
        .card-badge {{
            display: inline-block;
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 3px;
            margin-left: 6px;
            vertical-align: middle;
        }}
        .badge-ancestor {{
            background: #fefcbf;
            color: #744210;
            font-weight: bold;
        }}
        .chain-step {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 4px 0;
        }}
        .chain-line {{
            width: 2px;
            height: 18px;
            background: #a0aec0;
        }}
        .chain-label {{
            background: #edf2f7;
            border: 1px solid #cbd5e0;
            border-radius: 12px;
            padding: 2px 10px;
            font-size: 12px;
            font-weight: 500;
            color: #4a5568;
            margin: 2px 0;
        }}
        .empty-placeholder {{
            text-align: center;
            padding: 40px 20px;
            color: #718096;
            background: #f7fafc;
            border: 1px dashed #cbd5e0;
            border-radius: 6px;
        }}
    </style>
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
                    <li><a href="index.html" title="Surnames">Surnames</a></li>
                    <li><a href="interactive_graph.html" title="Interactive Graph">Interactive Graph</a></li>
                    <li class="CurrentSection"><a href="relationship.html" title="Relationship Finder">Relationship</a></li>
                </ul>
            </div>
        </div>
        <div class="content" id="RelationshipDetail">
            <h3>Relationship Finder</h3>
            <p>Select any two individuals below to trace their shortest genealogical connection, kinship title, and shared ancestors.</p>
            
            <div class="rel-controls">
                <div class="rel-field">
                    <label for="p1Input">Person 1:</label>
                    <input type="text" id="p1Input" list="peopleDatalist" placeholder="Search or type a name..." autocomplete="off" />
                </div>
                <button type="button" class="rel-btn" id="swapBtn" title="Swap individuals" onclick="swapPeople()">⇄</button>
                <div class="rel-field">
                    <label for="p2Input">Person 2:</label>
                    <input type="text" id="p2Input" list="peopleDatalist" placeholder="Search or type a name..." autocomplete="off" />
                </div>
                <button type="button" class="rel-btn rel-btn-primary" id="findBtn" onclick="onFindRelationship()">Find</button>
                <button type="button" class="rel-btn" id="clearBtn" onclick="clearForm()">Reset</button>
            </div>

            <div id="resultArea">
                <div id="emptyPlaceholder" class="empty-placeholder">
                    Select two people above and click <strong>Find</strong> to trace their relationship.
                </div>
                <div id="summaryCard" style="display: none;" class="rel-summary-box">
                    <div id="headline" class="rel-headline"></div>
                    <p id="metaInfo" class="rel-meta"></p>
                </div>
                <div id="chainContainer" class="chain-container" style="display: none;"></div>
            </div>

            <datalist id="peopleDatalist">
{people_datalist_options}
            </datalist>

            <script id="familyGraphData" type="application/json">
{graph_json}
            </script>
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
    <script>
    var graph = {{}};
    var nameLookup = {{}};

    function init() {{
        var raw = document.getElementById("familyGraphData").textContent;
        try {{
            graph = JSON.parse(raw);
        }} catch(e) {{
            console.error("Error parsing graph", e);
            return;
        }}
        for (var id in graph) {{
            var p = graph[id];
            nameLookup[p.name.toLowerCase()] = id;
        }}

        // Check URL parameters
        var params = new URLSearchParams(window.location.search);
        var p1 = params.get("p1");
        var p2 = params.get("p2");
        if (p1 && graph[p1]) {{
            document.getElementById("p1Input").value = formatPersonOption(graph[p1]);
        }}
        if (p2 && graph[p2]) {{
            document.getElementById("p2Input").value = formatPersonOption(graph[p2]);
        }}
        if (p1 && p2) {{
            onFindRelationship();
        }} else if (p1) {{
            document.getElementById("p2Input").focus();
        }}
    }}

    function formatPersonOption(p) {{
        var dates = "";
        if (p.birth || p.death) {{
            var b = p.birth ? "*" + p.birth : "";
            var d = p.death ? "+" + p.death : "";
            dates = " (" + [b, d].filter(Boolean).join(" ") + ")";
        }}
        return p.name + dates + " [" + p.id + "]";
    }}

    function resolveId(inputVal) {{
        if (!inputVal) return null;
        var trimmed = inputVal.trim();
        if (graph[trimmed]) return trimmed;
        var match = trimmed.match(/\\[([A-Za-z0-9_]+)\\]/);
        if (match && graph[match[1]]) return match[1];
        var lower = trimmed.toLowerCase();
        if (nameLookup[lower]) return nameLookup[lower];
        for (var id in graph) {{
            if (graph[id].name.toLowerCase() === lower) return id;
        }}
        return null;
    }}

    function swapPeople() {{
        var p1 = document.getElementById("p1Input").value;
        var p2 = document.getElementById("p2Input").value;
        document.getElementById("p1Input").value = p2;
        document.getElementById("p2Input").value = p1;
        if (p1 || p2) {{
            onFindRelationship();
        }}
    }}

    function clearForm() {{
        document.getElementById("p1Input").value = "";
        document.getElementById("p2Input").value = "";
        document.getElementById("emptyPlaceholder").style.display = "block";
        document.getElementById("emptyPlaceholder").innerHTML = "Select two people above and click <strong>Find</strong> to trace their relationship.";
        document.getElementById("summaryCard").style.display = "none";
        document.getElementById("chainContainer").style.display = "none";
        document.getElementById("chainContainer").innerHTML = "";
    }}

    function findShortestPath(startId, endId) {{
        if (startId === endId) return [startId];
        var queue = [[startId]];
        var visited = {{}};
        visited[startId] = true;

        while (queue.length > 0) {{
            var path = queue.shift();
            var currId = path[path.length - 1];
            var node = graph[currId];
            if (!node) continue;

            var neighbors = [];
            if (node.parents) neighbors.push.apply(neighbors, node.parents);
            if (node.children) neighbors.push.apply(neighbors, node.children);
            if (node.spouses) neighbors.push.apply(neighbors, node.spouses);

            for (var i = 0; i < neighbors.length; i++) {{
                var nextId = neighbors[i];
                if (nextId === endId) {{
                    var res = path.slice();
                    res.push(nextId);
                    return res;
                }}
                if (!visited[nextId] && graph[nextId]) {{
                    visited[nextId] = true;
                    var newPath = path.slice();
                    newPath.push(nextId);
                    queue.push(newPath);
                }}
            }}
        }}
        return null;
    }}

    function getStepLabel(curr, nxt) {{
        var nxtGender = nxt.gender || "unknown";
        if (curr.parents && curr.parents.indexOf(nxt.id) > -1) {{
            return {{
                dir: "up",
                arrow: "↑",
                text: nxtGender === "male" ? "Father of" : (nxtGender === "female" ? "Mother of" : "Parent of")
            }};
        }}
        if (curr.children && curr.children.indexOf(nxt.id) > -1) {{
            return {{
                dir: "down",
                arrow: "↓",
                text: nxtGender === "male" ? "Son of" : (nxtGender === "female" ? "Daughter of" : "Child of")
            }};
        }}
        if (curr.spouses && curr.spouses.indexOf(nxt.id) > -1) {{
            return {{
                dir: "lateral",
                arrow: "♥",
                text: nxtGender === "male" ? "Husband of" : (nxtGender === "female" ? "Wife of" : "Spouse of")
            }};
        }}
        return {{ dir: "other", arrow: "•", text: "Related to" }};
    }}

    function computeKinship(path) {{
        if (path.length === 1) return {{ title: "Self", commonAncestorId: null }};

        var p1 = graph[path[0]];
        var p2 = graph[path[path.length - 1]];
        var p2Gender = p2.gender || "unknown";

        var steps = [];
        for (var i = 0; i < path.length - 1; i++) {{
            var curr = graph[path[i]];
            var nxt = graph[path[i + 1]];
            var stepInfo = getStepLabel(curr, nxt);
            steps.push(stepInfo);
        }}

        // Direct ancestors
        var allUp = steps.every(function(s) {{ return s.dir === "up"; }});
        if (allUp) {{
            var dist = steps.length;
            var title;
            if (dist === 1) title = p2Gender === "male" ? "Father" : (p2Gender === "female" ? "Mother" : "Parent");
            else if (dist === 2) title = p2Gender === "male" ? "Grandfather" : (p2Gender === "female" ? "Grandmother" : "Grandparent");
            else if (dist === 3) title = p2Gender === "male" ? "Great-Grandfather" : (p2Gender === "female" ? "Great-Grandmother" : "Great-Grandparent");
            else {{
                var prefix = "";
                for (var k = 0; k < dist - 2; k++) prefix += "Great-";
                title = p2Gender === "male" ? prefix + "Grandfather" : (p2Gender === "female" ? prefix + "Grandmother" : prefix + "Grandparent");
            }}
            return {{ title: title, commonAncestorId: path[path.length - 1] }};
        }}

        // Direct descendants
        var allDown = steps.every(function(s) {{ return s.dir === "down"; }});
        if (allDown) {{
            var dist = steps.length;
            var title;
            if (dist === 1) title = p2Gender === "male" ? "Son" : (p2Gender === "female" ? "Daughter" : "Child");
            else if (dist === 2) title = p2Gender === "male" ? "Grandson" : (p2Gender === "female" ? "Granddaughter" : "Grandchild");
            else if (dist === 3) title = p2Gender === "male" ? "Great-Grandson" : (p2Gender === "female" ? "Great-Granddaughter" : "Great-Grandchild");
            else {{
                var prefix = "";
                for (var k = 0; k < dist - 2; k++) prefix += "Great-";
                title = p2Gender === "male" ? prefix + "Grandson" : (p2Gender === "female" ? prefix + "Granddaughter" : prefix + "Grandchild");
            }}
            return {{ title: title, commonAncestorId: path[0] }};
        }}

        // Spouse
        if (steps.length === 1 && steps[0].dir === "lateral") {{
            return {{ title: p2Gender === "male" ? "Husband" : (p2Gender === "female" ? "Wife" : "Spouse"), commonAncestorId: null }};
        }}

        // Blood relatives: Up to common ancestor, then down
        var upCount = 0;
        var downCount = 0;
        var phase = "up";
        var isBlood = true;
        var peakIdx = 0;
        for (var i = 0; i < steps.length; i++) {{
            if (steps[i].dir === "up") {{
                if (phase !== "up") {{ isBlood = false; break; }}
                upCount++;
                peakIdx = i + 1;
            }} else if (steps[i].dir === "down") {{
                phase = "down";
                downCount++;
            }} else {{
                isBlood = false;
                break;
            }}
        }}

        if (isBlood && upCount > 0 && downCount > 0) {{
            var commonId = path[peakIdx];
            if (upCount === 1 && downCount === 1) {{
                return {{ title: p2Gender === "male" ? "Brother" : (p2Gender === "female" ? "Sister" : "Sibling"), commonAncestorId: commonId }};
            }}
            if (upCount === 2 && downCount === 1) {{
                return {{ title: p2Gender === "male" ? "Uncle" : (p2Gender === "female" ? "Aunt" : "Aunt/Uncle"), commonAncestorId: commonId }};
            }}
            if (upCount === 1 && downCount === 2) {{
                return {{ title: p2Gender === "male" ? "Nephew" : (p2Gender === "female" ? "Niece" : "Niece/Nephew"), commonAncestorId: commonId }};
            }}
            if (upCount === 3 && downCount === 1) {{
                return {{ title: p2Gender === "male" ? "Great-Uncle" : (p2Gender === "female" ? "Great-Aunt" : "Great-Aunt/Uncle"), commonAncestorId: commonId }};
            }}
            if (upCount === 1 && downCount === 3) {{
                return {{ title: p2Gender === "male" ? "Great-Nephew" : (p2Gender === "female" ? "Great-Niece" : "Great-Niece/Nephew"), commonAncestorId: commonId }};
            }}

            var cDeg = Math.min(upCount, downCount) - 1;
            var rem = Math.abs(upCount - downCount);
            var degMap = {{ 1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th" }};
            var degName = degMap[cDeg] || (cDeg + "th");
            var title;
            if (rem === 0) {{
                title = degName + " Cousin";
            }} else {{
                var remMap = {{ 1: "once", 2: "twice", 3: "3 times", 4: "4 times" }};
                title = degName + " Cousin " + (remMap[rem] || (rem + " times")) + " removed";
            }}
            return {{ title: title, commonAncestorId: commonId }};
        }}

        // In-laws
        if (steps.length === 2 && steps[0].dir === "lateral" && steps[1].dir === "up") {{
            return {{ title: p2Gender === "male" ? "Father-in-law" : (p2Gender === "female" ? "Mother-in-law" : "Parent-in-law"), commonAncestorId: null }};
        }}
        if (steps.length === 2 && steps[0].dir === "down" && steps[1].dir === "lateral") {{
            return {{ title: p2Gender === "male" ? "Son-in-law" : (p2Gender === "female" ? "Daughter-in-law" : "Child-in-law"), commonAncestorId: null }};
        }}
        if (steps.length === 3 && steps[0].dir === "up" && steps[1].dir === "down" && steps[2].dir === "lateral") {{
            return {{ title: p2Gender === "male" ? "Brother-in-law" : (p2Gender === "female" ? "Sister-in-law" : "Sibling-in-law"), commonAncestorId: null }};
        }}
        if (steps.length === 3 && steps[0].dir === "lateral" && steps[1].dir === "up" && steps[2].dir === "down") {{
            return {{ title: p2Gender === "male" ? "Brother-in-law" : (p2Gender === "female" ? "Sister-in-law" : "Sibling-in-law"), commonAncestorId: null }};
        }}

        var hasSpouse = steps.some(function(s) {{ return s.dir === "lateral"; }});
        if (hasSpouse) {{
            return {{ title: "Relative by marriage (" + steps.length + " steps)", commonAncestorId: null }};
        }}
        return {{ title: "Relative (" + steps.length + " steps)", commonAncestorId: null }};
    }}

    function onFindRelationship() {{
        var id1 = resolveId(document.getElementById("p1Input").value);
        var id2 = resolveId(document.getElementById("p2Input").value);

        var emptyBox = document.getElementById("emptyPlaceholder");
        var summaryCard = document.getElementById("summaryCard");
        var chain = document.getElementById("chainContainer");

        if (!id1 || !id2) {{
            emptyBox.style.display = "block";
            emptyBox.innerHTML = "Please select both <strong>Person 1</strong> and <strong>Person 2</strong> from the list.";
            summaryCard.style.display = "none";
            chain.style.display = "none";
            return;
        }}

        if (id1 === id2) {{
            emptyBox.style.display = "block";
            emptyBox.innerHTML = "You have selected the same individual (<strong>" + graph[id1].name + "</strong>).";
            summaryCard.style.display = "none";
            chain.style.display = "none";
            return;
        }}

        var path = findShortestPath(id1, id2);
        if (!path) {{
            emptyBox.style.display = "block";
            emptyBox.innerHTML = "No genealogical connection was found between <strong>" + graph[id1].name + "</strong> and <strong>" + graph[id2].name + "</strong>.";
            summaryCard.style.display = "none";
            chain.style.display = "none";
            return;
        }}

        var kinshipInfo = computeKinship(path);
        renderPath(path, kinshipInfo);
    }}

    function renderPath(path, kinshipInfo) {{
        var p1 = graph[path[0]];
        var p2 = graph[path[path.length - 1]];

        document.getElementById("emptyPlaceholder").style.display = "none";
        var summaryCard = document.getElementById("summaryCard");
        summaryCard.style.display = "block";

        var headline = document.getElementById("headline");
        headline.textContent = p1.name + " is the " + kinshipInfo.title + " of " + p2.name;

        var metaInfo = document.getElementById("metaInfo");
        var metaParts = [(path.length - 1) + " step" + (path.length - 1 === 1 ? "" : "s") + " of separation"];
        if (kinshipInfo.commonAncestorId && graph[kinshipInfo.commonAncestorId]) {{
            var anc = graph[kinshipInfo.commonAncestorId];
            metaParts.push("Shared Ancestor: <a href='" + anc.path + "'>" + anc.name + "</a>");
        }}
        metaInfo.innerHTML = metaParts.join(" &bull; ");

        var chain = document.getElementById("chainContainer");
        chain.innerHTML = "";
        chain.style.display = "flex";

        for (var i = 0; i < path.length; i++) {{
            var person = graph[path[i]];
            var isCommonAnc = (person.id === kinshipInfo.commonAncestorId);

            var card = document.createElement("a");
            card.className = "person-card " + (person.gender || "") + (isCommonAnc ? " common-ancestor" : "");
            card.href = person.path;
            card.title = "View " + person.name;

            var nameDiv = document.createElement("div");
            nameDiv.className = "card-name";
            nameDiv.textContent = person.name;
            if (isCommonAnc) {{
                var badge = document.createElement("span");
                badge.className = "card-badge badge-ancestor";
                badge.textContent = "★ Common Ancestor";
                nameDiv.appendChild(badge);
            }}
            card.appendChild(nameDiv);

            var dates = [];
            if (person.birth) dates.push("*" + person.birth);
            if (person.death) dates.push("+" + person.death);
            if (dates.length > 0) {{
                var dateDiv = document.createElement("div");
                dateDiv.className = "card-dates";
                dateDiv.textContent = dates.join("  ");
                card.appendChild(dateDiv);
            }}

            chain.appendChild(card);

            if (i < path.length - 1) {{
                var nxtPerson = graph[path[i + 1]];
                var step = getStepLabel(person, nxtPerson);

                var stepDiv = document.createElement("div");
                stepDiv.className = "chain-step";

                var line1 = document.createElement("div");
                line1.className = "chain-line";
                stepDiv.appendChild(line1);

                var label = document.createElement("div");
                label.className = "chain-label";
                label.textContent = step.arrow + " " + step.text;
                stepDiv.appendChild(label);

                var line2 = document.createElement("div");
                line2.className = "chain-line";
                stepDiv.appendChild(line2);

                chain.appendChild(stepDiv);
            }}
        }}
    }}

    window.addEventListener("DOMContentLoaded", init);
    </script>
</body>
</html>
"""


INTERACTIVE_GRAPH_TEMPLATE = """<!DOCTYPE html>
<html xml:lang="en-GB" lang="en-GB" xmlns="http://www.w3.org/1999/xhtml">
<head lang="en-GB">
    <title>My Family Tree - Interactive Graph</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width; height=device-height; initial-scale=1.0; minimum-scale=0.5; maximum-scale=10.0; user-scalable=yes" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="generator" content="Gramps AIO64-5.1.5-1 http://gramps-project.org/" />
    <meta name="author" content="" />
    <link href="images/favicon2.ico" rel="shortcut icon" type="image/x-icon" />
    <link href="css/narrative-print.css" media="print" rel="stylesheet" type="text/css" />
    <link href="css/narrative-screen.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="css/interactive-graph.css" media="screen" rel="stylesheet" type="text/css" />
    <script>function navFunction() { var x = document.getElementById("dropmenu"); if (x.className === "nav") { x.className += " responsive"; } else { x.className = "nav"; } }</script>
</head>
<body id="InteractiveGraph">
    <div id="outerwrapper">
        <div id="header">
            <a href="javascript:void(0);" class="navIcon" onclick="navFunction()">&#8801;</a>
            <h1 id="SiteTitle">My Family Tree</h1>
        </div>
        <div class="wrappernav" id="nav" role="navigation">
            <div class="container">
                <ul class="nav" id="dropmenu">
                    <li><a href="individuals.html" title="Individuals">Individuals</a></li>
                    <li><a href="index.html" title="Surnames">Surnames</a></li>
                    <li class="CurrentSection"><a href="interactive_graph.html" title="Interactive Graph">Interactive Graph</a></li>
                    <li><a href="relationship.html" title="Relationship Finder">Relationship</a></li>
                </ul>
            </div>
        </div>
        <div class="content" id="InteractiveGraphDetail">
            <h2>Interactive Family Tree</h2>
            <div class="graph-toolbar">
                <div class="graph-tool-group">
                    <label for="viewSelect">View:</label>
                    <select id="viewSelect">
                        <option value="relatives" selected>Relatives</option>
                        <option value="hourglass">Hourglass</option>
                        <option value="ancestors">Ancestors</option>
                        <option value="descendants">Descendants</option>
                    </select>
                </div>
                <div class="graph-tool-group search-group">
                    <label for="personSearch">Person:</label>
                    <div class="search-input-wrapper">
                        <input type="text" id="personSearch" list="peopleDatalist" placeholder="Search person to center..." autocomplete="off" />
                        <button type="button" id="clearSearchBtn" class="clear-search-btn" title="Clear search" style="display: none;">&times;</button>
                    </div>
                </div>
                <div class="graph-tool-group">
                    <label for="colorSelect">Colors:</label>
                    <select id="colorSelect">
                        <option value="sex" selected>By Sex</option>
                        <option value="generation">By Generation</option>
                        <option value="none">Plain</option>
                    </select>
                </div>
                <div class="graph-tool-group graph-nav-controls">
                    <button type="button" class="graph-btn" id="homeBtn" title="Center on Emil Kerimov">&#127968; Emil</button>
                    <button type="button" class="graph-btn" id="fitViewBtn" title="Fit Entire Tree to Screen">Fit View</button>
                </div>
            </div>
            
            <div id="graph-container">
                <svg id="graph-svg">
                    <g id="zoom-layer">
                        <g id="tree-container"></g>
                    </g>
                </svg>

                <div id="person-popover" class="person-popover" style="display: none;">
                    <div class="popover-header">
                        <span id="popover-name" class="popover-name"></span>
                        <button type="button" id="popover-close" class="popover-close" title="Close">&times;</button>
                    </div>
                    <div id="popover-dates" class="popover-dates"></div>
                    <div class="popover-actions">
                        <a id="popover-view-btn" href="#" class="popover-btn primary-btn">View Profile &rarr;</a>
                        <button type="button" id="popover-center-btn" class="popover-btn">Center Tree Here</button>
                        <a id="popover-rel-btn" href="#" class="popover-btn">Find Relationship &rarr;</a>
                    </div>
                </div>
            </div>
            <p class="graph-hint">
                Click any person to view actions, or double-click to center on them. Drag canvas to pan, scroll to zoom.
            </p>

            <datalist id="peopleDatalist">
__PEOPLE_DATALIST_OPTIONS__
            </datalist>

            <script id="familyGraphData" type="application/json">
__GRAPH_JSON__
            </script>
            <script id="gedcomData" type="text/plain">
__GEDCOM_CONTENT__
            </script>
        </div>
        <div class="fullclear"></div>
        <div id="footer">
            <p id="createdate">
                Generated by <a href="http://gramps-project.org/">Gramps</a> AIO64-5.1.5-1 on 2025-03-23
            </p>
            <p id="copyright">
            </p>
        </div>
    </div>
    <script src="js/topola-bundle.min.js"></script>
    <script src="js/interactive_graph.js"></script>
</body>
</html>
"""
