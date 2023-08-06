import pytest
import sure

import datetime as dt

import obpy


def test_api_geojson_valid_city():
    ''' Check api_geojson handles a valid city. '''
    response = obpy.get_latest_geojson('toulouse')
    response.status_code.should.be.an(int)
    response.status_code.should.should.be.equal(200)


def test_api_geojson_invalid_city():
    ''' Check api_geojson handles an invalid city. '''
    response = obpy.get_latest_geojson('gnfkdgjldjls')
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(412)


def test_api_countries_valid_parameters():
    ''' Check api_countries handles all valid parameters. '''
    response = obpy.get_countries(provider='jcdecaux')
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_providers_valid_parameters():
    ''' Check api_providers handles all valid parameters. '''
    response = obpy.get_providers(country='France')
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_cities_valid_parameters():
    ''' Check api_cities handles all valid parameters. '''
    response = obpy.get_cities(slug='toulouse', predictable=1, active=1, country='France', provider='jcdecaux')
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_stations_valid_parameters():
    ''' Check api_stations handles all valid parameters. '''
    response = obpy.get_stations(slug='00003-pomme', city_slug='toulouse')
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_updates_all():
    ''' Check api_updates works with no parameters. '''
    response = obpy.get_updates()
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_metrics():
    ''' Check api_metrics works. '''
    response = obpy.get_metrics()
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_updates_valid_city():
    ''' Check api_updates handles valid city. '''
    response = obpy.get_updates(city_slug='toulouse')
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_filtered_without_forecasts():
    ''' Check api_filtered_stations works without forecasts. '''
    response = obpy.get_filtered_stations(
        city_slug='toulouse',
        latitude=43.6,
        longitude=1.4333,
        limit=1
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_filtered_with_forecasts():
    ''' Check api_filtered_stations works with forecasts. '''
    response = obpy.get_filtered_stations(
        city_slug='toulouse',
        latitude=43.6,
        longitude=1.4333,
        limit=1,
        kind='bikes',
        mode='walking',
        desired_quantity=1,
        moment=(dt.datetime.now() + dt.timedelta(minutes=1)).timestamp()
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_filtered_invalid_city():
    ''' Check api_filtered_stations handles invalid city names. '''
    response = obpy.get_filtered_stations(
        city_slug='xyz',
        latitude=43.6,
        longitude=1.4333,
        limit=1
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(412)


def test_api_closest_city():
    ''' Check api_closest_city works. '''
    response = obpy.get_closest_city(
        latitude='43.6',
        longitude='1.4333'
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_closest_station():
    ''' Check api_closest_station works. '''
    response = obpy.get_closest_station(
        latitude='43.6',
        longitude='1.4333'
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_forecast_invalid_city():
    ''' Check api_forecast handles invalid city. '''
    response = obpy.get_forecast(
        city_slug='xyz',
        station_slug='00003-pomme',
        kind='bikes',
        moment=(dt.datetime.now() + dt.timedelta(minutes=1)).timestamp()
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(412)


def test_api_forecast_invalid_station():
    ''' Check api_forecast handles invalid station. '''
    response = obpy.get_forecast(
        city_slug='toulouse',
        station_slug='xyz',
        kind='bikes',
        moment=(dt.datetime.now() + dt.timedelta(minutes=1)).timestamp()
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(412)


def test_api_forecast_invalid_kind():
    ''' Check api_forecast handles invalid kind. '''
    response = obpy.get_forecast(
        city_slug='toulouse',
        station_slug='00003-pomme',
        kind='xyz',
        moment=(dt.datetime.now() + dt.timedelta(minutes=1)).timestamp()
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(400)


def test_api_forecast_bikes():
    ''' Check api_forecast can forecast bikes. '''
    response = obpy.get_forecast(
        city_slug='toulouse',
        station_slug='00003-pomme',
        kind='bikes',
        moment=(dt.datetime.now() + dt.timedelta(minutes=1)).timestamp()
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)


def test_api_forecast_spaces():
    ''' Check api_forecast can forecast spaces. '''
    response = obpy.get_forecast(
        city_slug='toulouse',
        station_slug='00003-pomme',
        kind='spaces',
        moment=(dt.datetime.now() + dt.timedelta(minutes=1)).timestamp()
    )
    response.status_code.should.be.an(int)
    response.status_code.should.be.equal(200)
