from flask import jsonify, request, render_template
from src import app
from src.forms import LoginForm
from resources.assembly import Assembly_Data


# Helper Functions
def assemble_params(index1, index2, index3, index4, index5, index6):
    col_list = []
    hom_var = ['in_top25_hom', 'in_top10_hom', 'in_top5_hom', 'in_top1_hom']
    shoot_var = ['in_top25_shoot', 'in_top10_shoot', 'in_top5_shoot', 'in_top1_shoot']
    work_var = ['num_workers']
    edge_var = ['edges']
    if index1 == 'true':
        col_list = col_list+hom_var
    if index2 == 'true':
        col_list = col_list+shoot_var
    if index3 == 'true':
        pass
    if index4 == 'true':
        col_list = col_list+work_var
    if index5 == 'true':
        col_list = col_list+edge_var
    if index6 == 'true':
        pass
    print(col_list)
    return col_list


@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('main.html', form=form)


@app.route('/app')
def application():
    return render_template('view.html')


@app.route('/api', methods=['GET'])
def setup():
    map_setting = request.args.get('geo', None)
    outreach_var = int(request.args.get('outreach', None))
    allocation_var = int(request.args.get('allocation', None))
    homicide_set = request.args.get('h', None)
    shooting_set = request.args.get('s', None)
    census_set = request.args.get('c', None)
    outreach_set = request.args.get('o', None)
    edges_set = request.args.get('e', None)
    gangs_set = request.args.get('g', None)

    ad = Assembly_Data(map_setting)
    data = ad.my_assemblyData
    col_list = assemble_params(homicide_set, shooting_set,
                               census_set, outreach_set,
                               edges_set, gangs_set)
    data['Risk Score'] = data[col_list].sum(axis=1)
    my_riskScores = data[['beat_no','geometry','Risk Score']]
    my_riskScores = my_riskScores.sort_values(by=['Risk Score'], ascending=False)

    operator = round(outreach_var/allocation_var)
    print(operator)
    temp_df = my_riskScores.head(operator)
    first_ID_score = temp_df['Risk Score'].iloc[0]
    print(first_ID_score)
    if first_ID_score == 0:
        print("No input was provided, blank map returned")
        optimization = my_riskScores
    else:
        print("Custom map generated")
        optimization = temp_df
    optimization.to_file('Data/optimization.shp')
    optimization.to_file('maps/optimization.json', driver="GeoJSON")

    with open('maps/optimization.json', 'r') as original: data = original.read()
    with open('maps/optimization.json', 'w') as modified: modified.write("var optimizer = \n" + data)

    first_ID = str(optimization['beat_no'].iloc[0])
    first_ID_score = str(first_ID_score)

    return jsonify({first_ID:first_ID_score})
