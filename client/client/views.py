from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from client.application.clientmanager import ClientManager


def home(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        ClientManager.send_command(
            command='login',
            args=[request.POST.get('username'), request.POST.get('password')])

        response = ClientManager.receive_response()
        if response.get('success'):
            request.session['token'] = response.get('token')
            return HttpResponseRedirect('/map-selection/')

        return render(request, 'login.html', {'response': response})

    return render(request, 'login.html', {'response': ''})


def register(request):
    if request.method == 'POST':
        ClientManager.send_command(
            command='register',
            args=[request.POST.get('username'), request.POST.get('password')]
        )

        response = ClientManager.receive_response()
        if response.get('success'):
            return HttpResponseRedirect('/login/')

        return render(request, 'register.html', {'response': response})

    return render(request, 'register.html', {'response': ''})


def map_selection(request):
    maps_response = None

    if request.method == 'POST':
        if 'create_map' in request.POST:
            width = int(request.POST.get('width'))
            height = int(request.POST.get('height'))

            ClientManager.send_command(
                command='newmap',
                args=[f'{width}x{height}'],
                token=request.session.get('token')
            )

            response = ClientManager.receive_response()
            print(response)

        elif 'list_maps' in request.POST:
            ClientManager.send_command(
                command='showmaps',
                token=request.session.get('token')
            )

            response = ClientManager.receive_response()
            maps_response = response.get('maps')

        elif 'join' in request.POST:
            map_id = request.POST.get('selected-map')
            team_name = request.POST.get('team-name')
            ClientManager.send_command(
                command='join',
                args=[map_id, team_name],
                token=request.session.get('token')
            )
            join_response = ClientManager.receive_response()
            if join_response.get('success'):
                return redirect('game', map_id=map_id, team_name=team_name)

    return render(request, 'map-selection.html', {'maps_response': maps_response})


def game(request, map_id, team_name):
    if request.method == 'POST':
        direction = request.POST.get('direction')
        if direction:
            ClientManager.send_command(
                command='move',
                args=[direction],
                token=request.session.get('token')
            )
            move_response = ClientManager.receive_response()
            print(move_response)

        drop = request.POST.get('drop')
        if drop:
            ClientManager.send_command(
                command='drop',
                args=['b'],
                token=request.session.get('token')
            )
            drop_response = ClientManager.receive_response()
            print(drop_response)

    x_offset = 10
    y_offset = 10
    x_multiplier = 20
    y_multiplier = 20

    ClientManager.send_command(
        command='mapinfo',
        args=[map_id, team_name],
        token=request.session.get('token')
    )

    circle_list = [
        # {"x": 100, "y": 150, "color": "red", "size": 5, "label": "Test"},
    ]

    map_info_response = ClientManager.receive_response()

    for j in range(int(map_info_response.get('height'))):
        for i in range(int(map_info_response.get('width'))):
            circle_list.append(
                {"x": x_multiplier * i + x_offset,
                 "y": y_multiplier * j + y_offset,
                 "color": "LightGray",
                 "size": 2,
                 "label": ''},
            )

    for [x, y] in map_info_response.get('visible-positions'):
        circle_list.append(
            {"x": x_multiplier * x + x_offset,
             "y": y_multiplier * y + y_offset,
             "color": "Black",
             "size": 2,
             "label": ''},
        )

    for m in map_info_response.get('players'):
        circle_list.append(
            {"x": x_multiplier * int(m.get('x')) + x_offset,
             "y": y_multiplier * int(m.get('y')) + y_offset,
             "color": "red",
             "size": 5,
             "label": m.get('name')},
        )

    for m in map_info_response.get('explosives'):
        circle_list.append(
            {"x": x_multiplier * int(m.get('x')) + x_offset,
             "y": y_multiplier * int(m.get('y')) + y_offset,
             "color": "yellow",
             "size": 5,
             "label": m.get('name')},
        )

    return render(request, 'game.html', {
        'circle_list': circle_list,
        'svg_width': int(map_info_response.get('width')) * x_multiplier + x_offset,
        'svg_height': int(map_info_response.get('height')) * y_multiplier + y_offset,
    })
