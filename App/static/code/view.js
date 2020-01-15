function activeSelect(item) {
    if (item === 'geo') {
        document.getElementById("geo").classList.add("active");
        document.getElementById("var").classList.remove("active");
        document.getElementById("data").classList.remove("active");
        document.getElementById("geo-item").classList.remove("invisible");
        document.getElementById("null-item").classList.add("invisible");
        document.getElementById("var-item").classList.add("invisible");
        document.getElementById("data-item").classList.add("invisible");
    }
    if (item === 'var') {
        document.getElementById("var").classList.add("active");
        document.getElementById("geo").classList.remove("active");
        document.getElementById("data").classList.remove("active");
        document.getElementById("geo-item").classList.add("invisible");
        document.getElementById("var-item").classList.remove("invisible");
        document.getElementById("data-item").classList.add("invisible");
        document.getElementById("null-item").classList.add("invisible");
    }
    if (item === 'data') {
        document.getElementById("data").classList.add("active");
        document.getElementById("var").classList.remove("active");
        document.getElementById("geo").classList.remove("active");
        document.getElementById("geo-item").classList.add("invisible");
        document.getElementById("var-item").classList.add("invisible");
        document.getElementById("data-item").classList.remove("invisible");
        document.getElementById("null-item").classList.add("invisible");
    }
    if (item === 'beats') {
        document.getElementById("beats").classList.add("geo-active");
        document.getElementById("districts").classList.remove("geo-active");
        document.getElementById("neighborhoods").classList.remove("geo-active");
        return "beat";
    }
    if (item === 'districts') {
        document.getElementById("districts").classList.add("geo-active");
        document.getElementById("beats").classList.remove("geo-active");
        document.getElementById("neighborhoods").classList.remove("geo-active");
        return "district";
    }
    if (item === 'neighborhoods') {
        document.getElementById("neighborhoods").classList.add("geo-active");
        document.getElementById("districts").classList.remove("geo-active");
        document.getElementById("beats").classList.remove("geo-active");
        return "neighborhood";
    }
    else {
        console.log("The input is not a valid HTML ID");
    }
}

function async_head() {
    var script = document.createElement("script");
    script.src = "maps/optimization.json";
    script.async = true; //asynchronous
    document.getElementsByTagName("head")[0].appendChild(script);
}

function setGeo(carryon) {
    console.log(carryon);
    var geoset = document.getElementById('geoset');
    if (typeof(carryon === 'string')) {
        geoset.innerHTML = carryon;
    }
    else {
        geoset.innerHTML = 'Unassigned';
    }
}

function myswitch(item, command) {
    var onswitch = document.getElementById(item+'SwitchOn');
    var offswitch = document.getElementById(item+'SwitchOff');
    var switchTarget = document.getElementById(item+'Target');
    if (command === 'on') {
        onswitch.classList.add('sOn');
        offswitch.classList.remove('sOn');
        return true;
        switchTarget.classList.remove('invisible');
    }
    if (command === 'off') {
        onswitch.classList.remove('sOn');
        offswitch.classList.add('sOn');
        return false;
        switchTarget.classList.add('invisible');
    }
}

function flip(aBool) {
    aBool = true;
    return aBool;
} 

function update_switches(los_switches, update, index) {
    los_switches[index] = update;
    return los_switches;
}

function add_layer(base_bool, carryon, los_switches) {
    var outreachID = document.getElementById("outreachInput");
    var alloID = document.getElementById("allocationInput");
    if (base_bool === false) {
        console.log("No geographic variable has been set");
    }
    else {

        // parameters
        var gSetting = carryon;
        var outreach = outreachID.value.toString();
        console.log(outreach);
        var allocation = alloID.value.toString();
        console.log(allocation);
        var homicides = los_switches[0].toString();
        var shootings = los_switches[1].toString();
        var census = los_switches[2].toString();
        var outreach_presence = los_switches[3].toString();
        var edges = los_switches[4].toString();
        var gangs = los_switches[5].toString();

        // url construction
        var origin = 'http://localhost:5000/api';

        var url_1 = '?geo='+gSetting+'&outreach='+outreach+'&allocation='+allocation;
        var url_2 = '&h='+homicides+'&s='+shootings+'&c='+census+'&o='+outreach_presence;
        var url_3 = '&e='+edges+'&g='+gangs;

        var finalcall = origin+url_1+url_2+url_3;

        // fetch call
        fetch(finalcall, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
            .then(result => result.json())
            .then(item => {
                console.log(item);
                //rerender_map(carryon);
            })
            .catch(e => {
                console.log(e);
                return e;
            })

    }
}

function render_map(geokey) {
        var width = 800;
        var height = 580;
        if (geokey === 'base') {
            var myJson = city;
        }
        if (geokey === 'beat') {
            var myJson = beats_json;
        }
        if (geokey === 'district') {
            var myJson = districts_json;
        }
        if (geokey === 'neighborhood') {
            var myJson = sectors_json;
        }


        // Creates SVG
        var svg = d3.select("#map")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        // Append empty placeholder g element to the SVG
        // g will contain the geometry elements
        var g = svg.append("g");

        // width and height of the whole visualization
        // set projection parameters
        var chicago_lat = 41.878;
        var chicago_long = 87.6298;
        var albersProjection = d3.geoAlbers()
            // set scale of the map
            .scale( 85000 )
            .rotate( [chicago_long, 0] )
            .center( [0, chicago_lat] )
            .translate( [width/1.5, height/2.6 ]);

        // d3.geoPath displays data and generates a SVG shape 
        var geoPath = d3.geoPath()
            .projection( albersProjection );

        g.selectAll( "path" )
            .data( myJson.features )
            .enter()
            .append( "path" )
            .attr( "fill", "#ccc" )
            .attr( "stroke", "#333" )
            .attr( "d", geoPath );

}

function rerender_map(geokey) {
        console.log("Rerendering the map");
        var width = 800;
        var height = 580;
        if (geokey === 'base') {
            var myJson = city;
        }
        if (geokey === 'beat') {
            var myJson = beats_json;
        }
        if (geokey === 'district') {
            var myJson = districts_json;
        }
        if (geokey === 'neighborhood') {
            var myJson = sectors_json;
        }


        // Creates SVG
        var svg = d3.select("#map")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        // Append empty placeholder g element to the SVG
        // g will contain the geometry elements
        var g = svg.append("g");

        // width and height of the whole visualization
        // set projection parameters
        var chicago_lat = 41.878;
        var chicago_long = 87.6298;
        var albersProjection = d3.geoAlbers()
            // set scale of the map
            .scale( 85000 )
            .rotate( [chicago_long, 0] )
            .center( [0, chicago_lat] )
            .translate( [width/1.5, height/2.6 ]);

        // d3.geoPath displays data and generates a SVG shape 
        var geoPath = d3.geoPath()
            .projection( albersProjection );

        g.selectAll( "path" )
            .data( myJson.features )
            .enter()
            .append( "path" )
            .attr( "fill", "#ccc" )
            .attr( "stroke", "#333" )
            .attr( "d", geoPath );

        var optimized_beats = svg.append( "g" );

        optimized_beats.selectAll( "path" )
            .data(optimizer.features)
            .enter()
            .append("path")
            .attr( "fill", "#900" )
            .attr( "stroke", "#999" )
            .attr( "d", geoPath );

}