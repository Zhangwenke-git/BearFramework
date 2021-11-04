# -*- coding=utf-8 -*-

from tools.ParseXml import PraseXml

data = {
    "pyfile": "pyfilename",
    "start": "2020-12-13 03:34:34",
    "durations": "153.23",
    "total": "19",
    "passed": "12",
    "failed": "3",
    "errors": "3",
    "skipped": "4",
    "minimum": "1.23",
    "maximum": "12.5",
    "environment": {'Author': 'ZWK', 'Environment': 'UAT4', 'Server': '200.31.153.26'},
    "data": [
        {
            "scenario": "TestCase_GeneralOrder",
            "cases": [
                {
                    "name": "submitOrder",
                    "duration": "12.21",
                    "outcome": "Passed",
                    "times": "1",
                    "errors": ""
                },
                {
                    "name": "myOrder",
                    "duration": "1.21",
                    "outcome": "Passed",
                    "times": "1",
                    "errors": ""
                },
                {
                    "name": "queryOrder",
                    "duration": "4.21",
                    "outcome": "Failed",
                    "times": "1",
                    "errors": "There is an error!"
                },
                {
                    "name": "queryDeal",
                    "duration": "7.71",
                    "outcome": "Skipped",
                    "times": "1",
                    "errors": "There is a skipped case!"
                },
            ],
        }, {
            "scenario": "TestCase_FlexibleOrder",
            "cases": [
                {
                    "name": "submitOrder",
                    "duration": "1.21",
                    "outcome": "Skipped",
                    "times": "1",
                    "errors": "There is a skipped case!",
                    "detail": "There is a detail",
                },
                {
                    "name": "myOrder",
                    "duration": "1.21",
                    "outcome": "Skipped",
                    "times": "1",
                    "errors": "There is a skipped case!",
                    "detail": "There is a detail",
                },
                {
                    "name": "queryOrder",
                    "duration": "4.21",
                    "outcome": "Skipped",
                    "times": "1",
                    "errors": "There is a skipped case!",
                    "detail": "There is a detail",
                },

            ],
        },
        {
            "scenario": "TestCase_SSQOrder",
            "cases": [
                {
                    "name": "submitOrder",
                    "duration": "1.21",
                    "outcome": "Error",
                    "times": "1",
                    "errors": "There is a Error case!",
                    "detail": "There is a detail",
                },
                {
                    "name": "myOrder",
                    "duration": "1.21",
                    "outcome": "Error",
                    "times": "1",
                    "errors": "There is a Error case!",
                    "detail": "There is a detail",
                },
                {
                    "name": "queryOrder",
                    "duration": "4.21",
                    "outcome": "Skipped",
                    "times": "1",
                    "errors": "There is a skipped case!",
                    "detail": "There is a detail",
                },

            ],
        },

        {
            "scenario": "TestCase_SzxOrder",
            "cases": [
                {
                    "name": "submitOrder",
                    "duration": "12.21",
                    "outcome": "Passed",
                    "times": "1",
                    "errors": ""
                },
                {
                    "name": "myOrder",
                    "duration": "1.21",
                    "outcome": "Passed",
                    "times": "1",
                    "errors": "",
                    "detail": "There is a detail",
                },
                {
                    "name": "queryOrder",
                    "duration": "14.21",
                    "outcome": "Passed",
                    "times": "1",
                    "errors": "",
                    "detail": "There is a detail",
                },
                {
                    "name": "queryDeal",
                    "duration": "7.71",
                    "outcome": "Passed",
                    "times": "1",
                    "errors": "",
                    "detail": "There is a detail",
                },
            ],
        }
    ]
}


class AntReport():

    def _generateReportStyleAnt(self, data: dict, report_path):

        pyfile = data["pyfile"]
        start = data["start"]
        durations = float(data["durations"])
        total = int(data["total"])
        passed = int(data["passed"])
        failed = int(data["failed"])
        skipped = int(data["skipped"])
        minimum = float(data["minimum"])
        maximum = float(data["maximum"])
        environment = data["environment"]
        passedRate = float('%.2f' % ((passed / total) * 100))
        average = float('%.2f' % (durations / total))

        html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
    <META http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>TestResults</title>
    <style type="text/css">
        body {
            font: normal 68%% verdana, arial, helvetica;
            color: #000000;
        }

        table tr td, table tr th {
            font-size: 68%%;
        }

        table.details tr th {
            color: #ffffff;
            font-weight: bold;
            text-align: center;
            background: #2674a6;
            white-space: nowrap;
        }

        td.passed {
            color: green;
            font-weight: bold;
        }
        
        td.failed {
            color: red;
            font-weight: bold;
        }
        
        td.skipped {
            color: orange;
            font-weight: bold;
        }
        
        table.details tr td {
            background: #eeeee0;
            white-space: nowrap;
        }

        h1 {
            margin: 0 0 5px;
            font: 165%% verdana, arial, helvetica
        }

        h2 {
            margin-top: 1em;
            margin-bottom: 0.5em;
            font: bold 125%% verdana, arial, helvetica
        }

        h3 {
            margin-bottom: 0.5em;
            font: bold 115%% verdana, arial, helvetica
        }

        .Failure {
            font-weight: bold;
            color: red;
        }


        img {
            border-width: 0;
        }

        .expand_link {
            position : absolute;
            right: 0;
            width: 27px;
            top: 1px;
            height: 27px;
        }

        .page_details {
            display: none;
        }

        .page_details_expanded {
            display: block;
            display /* hide this definition from  IE5/6 */: table-row;
        }

        .log:only-child {
            height: inherit
        }
        .log {
            background-color: #e6e6e6;
            border: 1px solid #e6e6e6;
            color: black;
            display: block;
            font-family: "Courier New", Courier, monospace;
            height: 230px;
            overflow-y: scroll;
            padding: 5px;
            white-space: pre-wrap
        }
        
        



    </style>
    <script language="JavaScript">
        function expand(details_id) {

            document.getElementById(details_id).className = "page_details_expanded";
        }

        function collapse(details_id) {

            document.getElementById(details_id).className = "page_details";
        }

        function change(details_id) {
            if (document.getElementById(details_id + "_image").src.match("expand")) {
                document.getElementById(details_id + "_image").src = "collapse.png";
                expand(details_id);
            } else {
                document.getElementById(details_id + "_image").src = "expand.png";
                collapse(details_id);
            }
        }
    </script>
</head>
<body>
<h1>%s</h1>
<table width="100%%">
    <tr>
        <td align="left">Date report: %s</td>
        <td align="right">Environment: %s</td>
    </tr>
</table>
<hr size="1">
<h2>Summary</h2>
<table width="95%%" cellspacing="2" cellpadding="5" border="0" class="details" align="center">
    <tr valign="top">
        <th>Total</th>
        <th>Failures</th>
        <th>Pass</th>
        <th>Skip</th>
        <th>Success Rate</th>
        <th>Average Time</th>
        <th>Min Time</th>
        <th>Max Time</th>
        <th>Environment</th>
    </tr>
    <tr valign="top" class="" style="font-weight:bold">
        <td align="center" style="color:yellow">%d</td>
        <td align="center" style="color:red">%d</td>
        <td align="center" style="color:green">%d</td>
        <td align="center" style="color:orange">%d</td>
        <td align="center">%s%%</td>
        <td align="center">%s ms</td>
        <td align="center">%s ms</td>
        <td align="center">%s ms</td>
        <td align="center"><a href="">Environment Link</td>
    </tr>
</table>
<hr align="center" width="95%%" size="1">
<h2>Pages</h2>
<table width="95%%" cellspacing="2" cellpadding="5" border="0" class="details" align="center">
    <tr valign="top">
        <th>Order</th>
        <th>Scenario</th>
        <th>Failures</th>
        <th>Pass</th>
        <th>Skip</th>
        <th>Success Rate</th>
        <th>Average Time</th>
        <th>Min Time</th>
        <th>Max Time</th>
        <th>Outcome</th>
        <th></th>
    </tr>
        
        ''' % (pyfile, start, environment, total, failed, passed, skipped, passedRate, average, minimum, maximum)

        for scenario in data["data"]:
            scenarioNm, description, cases = scenario.get("scenario"), scenario.get("description"), scenario.get(
                "cases")
            index = data["data"].index(scenario) + 1
            duration_list, outcome_list = [float(case.get("duration")) for case in cases], [case.get("outcome") for case
                                                                                            in cases]

            total = len(duration_list)
            max_time, min_time, aver_time = max(duration_list), min(duration_list), float(
                '%.2f' % (sum(duration_list) / total))

            passed, failed, skipped = outcome_list.count("Passed"), outcome_list.count("Failed"), outcome_list.count(
                "Skipped")

            passedRt = float('%.2f' % ((passed / total) * 100))

            if passed == total:
                color, flag = 'passed', '√'
            elif skipped == total:
                color, flag = 'skipped', '∅'
            else:
                color, flag = 'failed', '×'

            html += '''
            
                <tr valign="top">
                <td align="center">%d</td>
                <td><b>%s</b></td>
                <td align="center">%d</td>
                <td align="center">%d</td>
                <td align="center">%d</td>
                <td align="center"><b>%s%%</b></td>
                <td align="right">%s ms</td>
                <td align="right">%sms</td>
                <td align="right">%s ms</td>
                <td align="center" class = "%s"><b>%s</b></td>
                <td align="center"><a href="javascript:change('page_details_%d')"><img alt="expand/collapse" src="expand.png"
                                                                                      id="page_details_%d_image"></a></td>
                </tr>
                <tr class="page_details" id="page_details_%d">
                    <td bgcolor="#FF0000" colspan="11">
                        <div align="center">
                            <b>Details for Page "%s"</b>
                            <table width="95%%" cellspacing="1" cellpadding="2" border="0" bgcolor="#2674A6" bordercolor="#000000">
                                <tr>
                                    <th>Order</th>
                                    <th>Case</th>
                                    <th>Iteration</th>
                                    <th>Time (milliseconds)</th>
                                    <th>Result</th>
                                    <th></th>
                                    
                                </tr>
            
            ''' % (
                index, scenarioNm, failed, passed, skipped, passedRt, aver_time, min_time, max_time, color,
                flag,
                index, index, index, scenarioNm)

            case_string = ''
            for case in cases:
                name, duration, outcome, times, errors, detail, parameter = case.get("name"), case.get(
                    "duration"), case.get(
                    "outcome"), case.get(
                    "times"), case.get("errors"), case.get("detail"), case.get("parameter")
                order = str(index) + "-" + str(cases.index(case) + 1)
                if outcome == "Passed":
                    color, display = 'passed', 'display:None'
                elif outcome == "Failed":
                    color, display = 'failed', ''
                else:
                    color, display = 'skipped', ''

                case_string += '''
                
                    <tr>
                        <td align="center">%s</td>
                        <td >%s</td>
                        <td align="center">%s</td>
                        <td align="right">%s</td>
                        <td align="center" class="%s">%s</td>
                        <td align="center"><a style="%s" href="javascript:change('page_details_%s')"><img alt="expand/collapse" src="expand.png"
                                                                                      id="page_details_%s_image" ></a></td>
                   
                    </tr>
                    
                    <tr class="page_details" style="%s" id="page_details_%s">
                    <td bgcolor="#FF0000" colspan="6">
                        <div align="center">
                            <table width="95%%" cellspacing="1" cellpadding="2" border="0" bgcolor="#2674A6" bordercolor="#000000">
                                <tr style="margin-bottom:10px">
                                    <td style="white-space: normal;color:red;"><b>%s</b></td>
                                </tr>
                                
                                <tr style="margin-bottom:10px">
                                    <td style="white-space: normal;color:orange;">%s</td>
                                </tr>
                                
                                <tr>
                                    
                                    <td class="extra" colspan="6">
                                        <div class="log">%s</div>
                                    </td>

                                </tr>
                            </table>
                        </div>
                    </td>
                    </tr>
                
                ''' % (
                    order, name, times, duration, color, outcome, display, order, order, display, order, errors,
                    parameter,
                    detail)
            case_string += '''</table></div></td></tr>'''

            html += case_string
        html += '''     </table>
                        <hr align="center" width="95%" size="1">
                        </body>
                    </html>
              '''

        with open('%s.html' % pyfile, 'w', encoding="utf-8") as f:
            f.write(html)
        return html

    def _generateReportStyleHtml(self, data: dict, report_path):

        pyfile = data["pyfile"]
        start = data["start"]
        durations = float(data["durations"])
        total = int(data["total"])
        passed = int(data["passed"])
        errors = int(data["errors"])
        failed = int(data["failed"])
        skipped = int(data["skipped"])
        minimum = float(data["minimum"])
        maximum = float(data["maximum"])
        environment = data["environment"]
        passedRate = float('%.2f' % ((passed / total) * 100))
        average = float('%.2f' % (durations / total))
        environment_string = ""
        if isinstance(environment, dict):

            for key, value in environment.items():
                environment_string += '''
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>

                ''' % (key, value)

        html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8"/>
                <title>Pytest ant Html-ZWK</title>
                <style>body {
                    font-family: Helvetica, Arial, sans-serif;
                    font-size: 13px;
                    /* do not increase min-width as some may use split screens */
                    min-width: 800px;
                    color: #999;
                }
            
                h1 {
                    font-size: 26px;
                    color: black;
                }
            
                h2 {
                    font-size: 18px;
                    color: black;
                }
            
                p {
                    color: black;
                }
            
                a {
                    color: #999;
                }
            
                table {
                    border-collapse: collapse;
                }
            
                /******************************
                 * SUMMARY INFORMATION
                 ******************************/
            
                #environment td {
                    padding: 5px;
                    border: 1px solid #E6E6E6;
                }
            
                #environment tr:nth-child(odd) {
                    background-color: #f6f6f6;
                }
            
                /******************************
                 * TEST RESULT COLORS
                 ******************************/
                span.passed {
            
                    color: green;
                    border-radius: 12px;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid green;
            
                }
            
                span.skipped, span.xfailed, span.skipped {
                    color: gray;
                    border-radius: 12px;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid gray;
                }
            
                span.failed, span.xpassed {
                    color: red;
                    border-radius: 12px;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid red;
                }
                
                span.error {
                    color: orange;
                    border-radius: 12px;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid orange;
                }
            
            
                .passed .col-result {
                    color: green;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid green;
            
                }
            
                .skipped .col-result, .xfailed .col-result, .skipped .col-result {
                    color: gray;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid gray;
                }
            
                .failed .col-result, .xpassed .col-result {
                    color: red;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid red;
                }
                
                .error .col-result {
                    color: orange;
                    padding: 3px 14px;
                    cursor: pointer;
                    border: 1px solid orange;
                }
            
                /******************************
                 * RESULTS TABLE
                 *
                 * 1. Table Layout
                 * 2. Extra
                 * 3. Sorting items
                 *
                 ******************************/
            
                /*------------------
                 * 1. Table Layout
                 *------------------*/
            
                #results-table {
                    border: 1px solid #e6e6e6;
                    color: black;
                    font-size: 12px;
                    width: 100%%
                }
            
                #results-table th {
                    padding: 5px;
                    border: 1px solid #E6E6E6;
                    text-align: center;
                    background: #2674a6;
                    white-space: nowrap;
                    font-weight: bolder;
                    font-size: 15px;
                    color:white;
                }
            
            
                #results-table td {
                    padding: 5px;
                    border: 1px solid #E6E6E6;
                    background: #eeeee0;
                    white-space: nowrap;
                }
            
                /*------------------
                 * 2. Extra
                 *------------------*/
            
                .log:only-child {
                    height: inherit
                }
            
                .log {
                    background-color: #e6e6e6;
                    border: 1px solid #e6e6e6;
                    color: black;
                    display: block;
                    font-family: "Courier New", Courier, monospace;
                    height: 230px;
                    overflow-y: scroll;
                    padding: 2px;
                    white-space: pre-wrap
                }
            
                div.image {
                    border: 1px solid #e6e6e6;
                    float: right;
                    height: 240px;
                    margin-left: 5px;
                    overflow: hidden;
                    width: 320px
                }
            
                div.image img {
                    width: 320px
                }
            
                .collapsed {
                    display: none;
                }
            
                .expander::after {
                    content: " (show)";
                    color: #BBB;
                    font-style: italic;
                    cursor: pointer;
                }
            
                .collapser::after {
                    content: " (hide)";
                    color: #BBB;
                    font-style: italic;
                    cursor: pointer;
                }
            
                /*------------------
                 * 3. Sorting items
                 *------------------*/
                .sortable {
                    cursor: pointer;
                }
            
                .sort-icon {
                    font-size: 0px;
                    float: left;
                    margin-right: 5px;
                    margin-top: 5px;
                    /*triangle*/
                    width: 0;
                    height: 0;
                    border-left: 8px solid transparent;
                    border-right: 8px solid transparent;
                }
            
                .inactive .sort-icon {
                    /*finish triangle*/
                    border-top: 8px solid #E6E6E6;
                }
            
                .asc.active .sort-icon {
                    /*finish triangle*/
                    border-bottom: 8px solid #999;
                }
            
                .desc.active .sort-icon {
                    /*finish triangle*/
                    border-top: 8px solid #999;
                }
            
                table.details tr td {
                    background: #eeeee0;
                    white-space: nowrap;                   
                }
            
            
                table.details tr th {
                    color: #ffffff;
                    font-weight: bold;
                    text-align: center;
                    background: #2674a6;
                    white-space: nowrap;
                }
            
                .expand_link {
                    position: absolute;
                    right: 0;
                    width: 27px;
                    top: 1px;
                    height: 27px;
                }
            
                .page_details {
                    display: none;
                }
            
                .page_details_expanded {
                    display: block;
                    display /* hide this definition from  IE5/6 */: table-row;
                }
                td.passed {
                    color: green;
                    font-weight: bold;
                }
                
                td.failed {
                    color: red;
                    font-weight: bold;
                }
                
                td.skipped {
                    color: gray;
                    font-weight: bold;
                }
                
                td.error {
                    color: orange;
                    font-weight: bold;
                }
                
                table.loginfo {
                    border-collapse:separate;
                    border-spacing:0px 5px;
                    valign:top;
                    width:100%%;
                }
                
                tr.scenario {
                    color:black;
                    font-weight:bold;
                    font-family: "Microsoft YaHei";
                    font-size:15px;
                }
                
                tr.case {
                    font-size:13px;   
                }
                
                td #outcome {
                    font-weight:bold;
                    font-family: "Microsoft YaHei";
                    font-size:13px;
                }
                
            
                </style>
            </head>
            <body onLoad="init()">
            <script>/* This Source Code Form is subject to the terms of the Mozilla Public
             * License, v. 2.0. If a copy of the MPL was not distributed with this file,
             * You can obtain one at http://mozilla.org/MPL/2.0/. */
            
            
            function toArray(iter) {
                if (iter === null) {
                    return null;
                }
                return Array.prototype.slice.call(iter);
            }
            
            function find(selector, elem) {
                if (!elem) {
                    elem = document;
                }
                return elem.querySelector(selector);
            }
            
            function find_all(selector, elem) {
                if (!elem) {
                    elem = document;
                }
                return toArray(elem.querySelectorAll(selector));
            }
            
            function sort_column(elem) {
                toggle_sort_states(elem);
                var colIndex = toArray(elem.parentNode.childNodes).indexOf(elem);
                var key;
                if (elem.classList.contains('numeric')) {
                    key = key_num;
                } else if (elem.classList.contains('result')) {
                    key = key_result;
                } else {
                    key = key_alpha;
                }
                sort_table(elem, key(colIndex));
            }
            
            function show_all_extras() {
                find_all('.col-result').forEach(show_extras);
            }
            
            function hide_all_extras() {
                find_all('.col-result').forEach(hide_extras);
            }
            
            function show_extras(colresult_elem) {
                var extras = colresult_elem.parentNode.nextElementSibling;
                var expandcollapse = colresult_elem.firstElementChild;
                extras.classList.remove("collapsed");
                expandcollapse.classList.remove("expander");
                expandcollapse.classList.add("collapser");
            }
            
            function hide_extras(colresult_elem) {
                var extras = colresult_elem.parentNode.nextElementSibling;
                var expandcollapse = colresult_elem.firstElementChild;
                extras.classList.add("collapsed");
                expandcollapse.classList.remove("collapser");
                expandcollapse.classList.add("expander");
            }
            
            function show_filters() {
                var filter_items = document.getElementsByClassName('filter');
                for (var i = 0; i < filter_items.length; i++)
                    filter_items[i].hidden = false;
            }
            
            function add_collapse() {
                // Add links for show/hide all
                var resulttable = find('table#results-table');
                var showhideall = document.createElement("p");
                showhideall.innerHTML = '<button><a style="text-decoration:none;" href="javascript:show_all_extras()">EXPAND</a></button> / ' +
                    '<button><a style="text-decoration:none;" href="javascript:hide_all_extras()">COLLAPSE</a></button>';
                resulttable.parentElement.insertBefore(showhideall, resulttable);
            
                // Add show/hide link to each result
                find_all('.col-result').forEach(function (elem) {
                    var collapsed = get_query_parameter('collapsed') || 'Passed';
                    var extras = elem.parentNode.nextElementSibling;
                    var expandcollapse = document.createElement("span");
                    if (collapsed.includes(elem.innerHTML)) {
                        extras.classList.add("collapsed");
                        expandcollapse.classList.add("expander");
                    } else {
                        expandcollapse.classList.add("collapser");
                    }
                    elem.appendChild(expandcollapse);
            
                    elem.addEventListener("click", function (event) {
                        if (event.currentTarget.parentNode.nextElementSibling.classList.contains("collapsed")) {
                            show_extras(event.currentTarget);
                        } else {
                            hide_extras(event.currentTarget);
                        }
                    });
                })
            }
            
            function get_query_parameter(name) {
                var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
                return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
            }
            
            function init () {
                reset_sort_headers();
            
                add_collapse();
            
                show_filters();
            
                sort_column(find('.initial-sort'));
            
                find_all('.sortable').forEach(function(elem) {
                    elem.addEventListener("click",
                                          function(event) {
                                              sort_column(elem);
                                          }, false)
                });
            
            };
            
            function sort_table(clicked, key_func) {
                var rows = find_all('.results-table-row');
                var reversed = !clicked.classList.contains('asc');
                var sorted_rows = sort(rows, key_func, reversed);
                /* Whole table is removed here because browsers acts much slower
                 * when appending existing elements.
                 */
                var thead = document.getElementById("results-table-head");
                document.getElementById('results-table').remove();
                var parent = document.createElement("table");
                parent.id = "results-table";
                parent.appendChild(thead);
                sorted_rows.forEach(function(elem) {
                    parent.appendChild(elem);
                });
                document.getElementsByTagName("BODY")[0].appendChild(parent);
            }
            
            function sort(items, key_func, reversed) {
                var sort_array = items.map(function(item, i) {
                    return [key_func(item), i];
                });
            
                sort_array.sort(function(a, b) {
                    var key_a = a[0];
                    var key_b = b[0];
            
                    if (key_a == key_b) return 0;
            
                    if (reversed) {
                        return (key_a < key_b ? 1 : -1);
                    } else {
                        return (key_a > key_b ? 1 : -1);
                    }
                });
            
                return sort_array.map(function(item) {
                    var index = item[1];
                    return items[index];
                });
            }
            
            function key_alpha(col_index) {
                return function(elem) {
                    return elem.childNodes[1].childNodes[col_index].firstChild.data.toLowerCase();
                };
            }
            
            function key_num(col_index) {
                return function(elem) {
                    return parseFloat(elem.childNodes[1].childNodes[col_index].firstChild.data);
                };
            }
            
            function key_result(col_index) {
                return function(elem) {
                    var strings = ['Error', 'Failed', 'Rerun', 'XFailed', 'XPassed',
                                   'Skipped', 'Passed'];
                    return strings.indexOf(elem.childNodes[1].childNodes[col_index].firstChild.data);
                };
            }
            
            function reset_sort_headers() {
                find_all('.sort-icon').forEach(function(elem) {
                    elem.parentNode.removeChild(elem);
                });
                find_all('.sortable').forEach(function(elem) {
                    var icon = document.createElement("div");
                    icon.className = "sort-icon";
                    icon.textContent = "vvv";
                    elem.insertBefore(icon, elem.firstChild);
                    elem.classList.remove("desc", "active");
                    elem.classList.add("asc", "inactive");
                });
            }
            
            function toggle_sort_states(elem) {
                //if active, toggle between asc and desc
                if (elem.classList.contains('active')) {
                    elem.classList.toggle('asc');
                    elem.classList.toggle('desc');
                }
            
                //if inactive, reset all other functions and add ascending active
                if (elem.classList.contains('inactive')) {
                    reset_sort_headers();
                    elem.classList.remove('inactive');
                    elem.classList.add('active');
                }
            }
            
            function is_all_rows_hidden(value) {
              return value.hidden == false;
            }
            
            function filter_table(elem) {
                var outcome_att = "data-test-result";
                var outcome = elem.getAttribute(outcome_att);
                class_outcome = outcome + " results-table-row";
                var outcome_rows = document.getElementsByClassName(class_outcome);
            
                for(var i = 0; i < outcome_rows.length; i++){
                    outcome_rows[i].hidden = !elem.checked;
                }
            
                var rows = find_all('.results-table-row').filter(is_all_rows_hidden);
                var all_rows_hidden = rows.length == 0 ? true : false;
                var not_found_message = document.getElementById("not-found-message");
                not_found_message.hidden = !all_rows_hidden;
            }
            
            
            function expand(details_id) {
            
                document.getElementById(details_id).className = "page_details_expanded";
            }
            
            function collapse(details_id) {
            
                document.getElementById(details_id).className = "page_details";
            }
            
            function change(details_id) {
                if (document.getElementById(details_id + "_image").src.match("SuQmCC")) {
                    document.getElementById(details_id + "_image").src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAGUExURSZ0pv///xB+eSAAAAARSURBVAjXY2DABuR/gBA2AAAzpwIvNQARCgAAAABJRU5ErkJggg==";
                    expand(details_id);
                } else {
                    document.getElementById(details_id + "_image").src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAGUExURSZ0pv///xB+eSAAAAAWSURBVAjXY2CAAcYGBJL/AULIIjAAAJJrBjcL30J5AAAAAElFTkSuQmCC";
                    collapse(details_id);
                }
            }
            </script>
            <h1>Ant Style Pytest-html Report</h1>
            
            <h2>Environment</h2>
            <table id="environment"> 
                %s
                <tr>
                    <td>Startpoint</td>
                    <td>%s</td>
                </tr>
        
            </table>
            
            <h2>Summary</h2>
            <hr size="1">
            <table width="100%%" cellspacing="2" cellpadding="5" border="0" class="details" align="center">
                <tr valign="top">
                    <th>Total</th>
                    <th>Errors</th>
                    <th>Failures</th>
                    <th>Pass</th>
                    <th>Skip</th>
                    <th>Success Rate</th>
                    <th>Average Time</th>
                    <th>Min Time</th>
                    <th>Max Time</th>
            
                </tr>
                <tr valign="top" class="" style="font-weight:bold">
                    <td align="center" style="color:black">%d</td>
                    <td align="center" style="color:orange">%d</td>
                    <td align="center" style="color:red">%d</td>
                    <td align="center" style="color:green">%d</td>
                    <td align="center" style="color:gray">%d</td>
                    <td align="center">%s%%</td>
                    <td align="center">%s ms</td>
                    <td align="center">%s ms</td>
                    <td align="center">%s ms</td>
            
                </tr>
            </table>
            <hr align="center" width="100%%" size="1">
            
            
            <h2 class="filter" hidden="true">Filter</h2>
            <input checked="true" class="filter" data-test-result="passed" hidden="true" name="filter_checkbox"
                   onChange="filter_table(this)" type="checkbox"/><span class="passed">Passed</span>
            <input checked="true" class="filter" data-test-result="failed" hidden="true" name="filter_checkbox"
                   onChange="filter_table(this)" type="checkbox"/><span class="failed">Failed</span>
            <input checked="true" class="filter" data-test-result="skipped" hidden="true" name="filter_checkbox"
                   onChange="filter_table(this)" type="checkbox"/><span class="skipped">Skipped</span>
            <input checked="true" class="filter" data-test-result="error" hidden="true" name="filter_checkbox"
                   onChange="filter_table(this)" type="checkbox"/><span class="error">Errors</span>
            
            <h2>Pages</h2>
            <table id="results-table">
            
                <thead id="results-table-head">
                <tr>
                    <th class="sortable numeric" col="name">Order</th>
                    <th class="sortable" col="name">Scenario</th>
                    <th col="name">Errors</th>
                    <th col="name">Failures</th>
                    <th col="name">Pass</th>
                    <th col="name">Skip</th>
                    <th class="sortable numeric" col="name">Success Rate</th>
                    <th class="sortable numeric" col="time">Average Time</th>
                    <th col="time">Min Time</th>
                    <th col="time">Max Time</th>
                    <th class="sortable result initial-sort" col="result">Outcome</th>
            
                </tr>
                <tr hidden="true" id="not-found-message">
                    <th colspan="11">No results found. Please check the filters</th>
                </tr>
                </thead>
        
        
        ''' % (environment_string, start, total, errors, failed, passed, skipped, passedRate, average, minimum, maximum)

        for scenario in data["data"]:
            scenarioNm, description, cases = scenario.get("scenario"), scenario.get("description"), scenario.get(
                "cases")
            index = data["data"].index(scenario) + 1
            duration_list, outcome_list = [float(case.get("duration")) for case in cases], [case.get("outcome") for case
                                                                                            in cases]

            total = len(duration_list)
            max_time, min_time, aver_time = max(duration_list), min(duration_list), float(
                '%.2f' % (sum(duration_list) / total))

            passed, failed, skipped, error = outcome_list.count("Passed"), outcome_list.count(
                "Failed"), outcome_list.count(
                "Skipped"), outcome_list.count(
                "Error")

            passedRt = float('%.2f' % ((passed / total) * 100))


            if passed == total:
                # color, flag = 'passed', '√'
                color, flag = 'passed', '〓〓〓'
            elif skipped == total:
                # color, flag = 'skipped', '∅'
                color, flag = 'skipped', '〓〓〓'
            elif failed != 0:
                # color, flag = 'failed', '×'
                color, flag = 'failed', '〓〓〓'
            elif error != 0:
                color, flag = 'error', '〓〓〓'
            else:
                color, flag = '', ''

            html += '''
                <tbody class="%s results-table-row">
                <tr class="scenario">
                    <td class="col-name" align="center">%d</td>
                    <td class="col-name">%s</td>
                    <td class="col-name">%d</td>
                    <td class="col-name">%d</td>
                    <td class="col-name">%d</td>
                    <td class="col-name">%d</td>
                    <td class="col-name">%s%%</td>
                    <td class="col-time">%s ms</td>
                    <td class="col-duration">%s ms</td>
                    <td class="col-links">%s ms</td>
                    <td class="col-result">%s</td>
                </tr>
            
            
                <tr>
                    <td class="extra" colspan="11">
                        <div>
                            <table width="99%%" class="details" id="case">
                                <tr>
                                    <th>Order</th>
                                    <th>Case</th>
                                    <th>Iteration</th>
                                    <th>Time (milliseconds)</th>
                                    <th>Result</th>
                                    <th>Flag</th>
                                </tr>
            ''' % (color, index, scenarioNm, error, failed, passed, skipped, passedRt, aver_time, min_time, max_time, flag)

            case_string = ""
            for case in cases:
                name, duration, outcome, times, errors, detail, parameter,log = case.get("name"), case.get(
                    "duration"), case.get(
                    "outcome"), case.get(
                    "times"), case.get("errors"), case.get("detail"), case.get("parameter"),case.get("log")
                order = str(index) + "-" + str(cases.index(case) + 1)
                if outcome == "Passed":
                    color, display = 'passed', 'display:None'
                elif outcome == "Failed":
                    color, display = 'failed', ''
                elif outcome == "Error":
                    color, display = 'error', ''
                else:
                    color, display = 'skipped', ''

                case_string += '''

                    <tr class="case">
                        <td align="center">%s</td>
                        <td >%s</td>
                        <td align="center">%s</td>
                        <td align="right">%s</td>
                        <td align="center" id="outcome" class="%s">%s</td>
                        <td align="center"><a style="%s" href="javascript:change('page_details_%s')"><img alt="expand/collapse" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAGUExURSZ0pv///xB+eSAAAAAWSURBVAjXY2CAAcYGBJL/AULIIjAAAJJrBjcL30J5AAAAAElFTkSuQmCC"
                                                                                      id="page_details_%s_image" ></a></td>

                    </tr>

                    <tr class="page_details" style="%s" id="page_details_%s">
                        <td colspan="11">
                            <div class="log" align="center">

                                <table class="loginfo">
                                    <tr align="left" style="color: red;">
                                        <td style="white-space: normal;background-color:#faebd7;"><h3>Errors: </h3>'%s'</td>
                                    </tr>

                                    <tr>
                                        <td style="white-space: pre-wrap;background-color:#f5f5f5;"><h3 style="color:orange">Details:</h3> %s</td>
                                    </tr>
                                    
                                    <tr>
                                        <td style="white-space: pre-wrap;background-color:#f5f5f5;"><h3 style="color:blue">Logs:</h3> %s</td>
                                    </tr>

                                </table>
                            </div>
                        </td>
                    </tr>
                
   
                ''' % (
                    order, name, times, duration, color, outcome, display, order, order, display, order, errors, detail,log)
            case_string += '''</table>
                        </div>
                    </td>
                </tr>
            </tbody>'''

            html += case_string
        html += '''</table>
            </body>
        </html>'''

        report_path = r'%s\ant-html.html' % report_path
        with open(report_path, 'w', encoding="utf-8") as f:
            f.write(html)
        f.close()
        return html

    def antReport(self, report_path):
        xml_obj = PraseXml()
        data = xml_obj.readJunitXML(report_path)
        self._generateReportStyleHtml(data, report_path)


if __name__ == "__main__":
    html = AntReport()

    # data = xml_obj.readJunitXML(data_xml)
    #html._generateReportStyleHtml(data,r"C:\\Users\\ZWK\\Desktop\\AutomaticFramework\\report\\ant\\API\\20201219\\202012192253")
    html.antReport(r"C:\Users\ZWK\Desktop\AutomaticFramework\report\ant\API\20201225\202012252224")
