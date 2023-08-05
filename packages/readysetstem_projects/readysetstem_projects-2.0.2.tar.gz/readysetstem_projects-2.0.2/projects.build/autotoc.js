function generate_toc() {
    var pg_index = getFlowIndex();
    var autotoc = document.getElementsByClassName("autotoc")[0];

    // Calc size of each section.  For each pg_index item that has a 'section',
    // it is the number of entries up until the next section.
    var section_size = 0;
    var section_index = 0;
    for (var i = 0; i < pg_index.length; i++) {
        if ("section" in pg_index[i]) {
            if (i > 0) {
                pg_index[section_index].section_size = section_size;
            }
            section_size = 1;
            section_index = i;
        } else {
            section_size++;
        }
    }
    pg_index[section_index].section_size = section_size;

    var html = "";
    var index_header = document.getElementById("index_header");
    html += "<table id=index_table>";
        html += "<thead class=sticky>";
            html += "<tr class=content_row>";
                html += "<th class=section><p></p></th>";
                html += "<th>";
                    html += index_header.outerHTML;
                html += "</th>";
            html += "</tr>";
        html += "</thead>";
    html += "<tbody>";
    for (var i = 0; i < pg_index.length; i++) {
        row = pg_index[i];
        if ("section" in row) {
            if (i > 0) {
                html += "</tbody><tbody>";
            }
            html += "<tr class=content_row>";
            html += '<td class=section rowspan=' + row.section_size + '><p>'
                    + row.section + "</p></td>";
        } else {
            html += "<tr class=content_row>";
        }
        toc_type = row.concept ? 'concept' : 'project';
        first_project_arrow = i == 0 ? '<div id=firstproject>&#10137;</div>' : '';
        title_cell =
            '<td class="' + toc_type + '">'
                + '<a href="' + row.filename + '">'
                    + first_project_arrow
                    + '<p>'
                        + row.title
                        + '<span></span>' // Required to make container clickable - see CSS
                    + '</p>'
                + '</a>'
            + '</td>';
        html += title_cell;
        html += "</tr>";
    }
    html += "</tbody></table>";
    autotoc.innerHTML = html;
}

function newFlow() {
    // Using jquery to scroll to top
    $("body").animate({ scrollTop: 0 }, 1200);
    
    var flow = document.getElementById("flow");
    setFlowName(flow.value);
    generate_toc();
}

chainedOnload(function() {
    // Configure flow select box
    var flow = document.getElementById("flow");
    for (var f in pg_flows) {
        var option = document.createElement("option");
        option.text = f;
        flow.add(option);
    }

    // Restore default selection
    flow_name = getFlowName();
    if (flow_name.length > 0) {
        flow.value = flow_name;
    } else {
        flow.options[0].selected = true;
    }

    generate_toc();
});
