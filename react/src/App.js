import React from 'react';
import logo from './clock.png';
// import 
import './App.css';

export default class App extends React.Component {


  render() {
    var lat = 0;
    var lng = 0;
    async function displayLocationInfo(position) {
      let x = document.getElementsByClassName("time");
      if (navigator.geolocation) {
        await navigator.geolocation.getCurrentPosition(getData);
      } else {
        x[0].innerHTML = "Geolocation is not supported by this browser.";
      }
    }

    async function getData(position) {
      let x = document.getElementsByClassName("time");
      lat = await position.coords.latitude;
      lng = await position.coords.longitude;
      try {
        var json = {
          location: {
            long: lng,
            lat: lat
          }
        };
        var data = JSON.stringify(json);
        //ENTER API LINK HERE
        let response = await fetch('API_LINK', {
          method: 'POST',
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: data
        })

        let responseJson = await response.json();

        x[0].innerText = responseJson['time_zone'] + '\n' + responseJson['time'];
        x[1].innerText = "Latitude: " + lat + "\nLongitude: " + lng + "\n" + responseJson['loc_name'];
      }
      catch (error) {
        alert(error);
      }
    };
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />

          <p className="time">
            Click to get ur timezone!
          </p>
          <p className="time" id="location">
            Your location will show up here
          </p>

          <h1 >
            <button className="square" onClick={displayLocationInfo}>
              Time
      </button>
          </h1>

          <a className="App-link"
            href="/"
            rel="noopener noreferrer">
            restart
          </a>
        </header>
      </div>
    );
  }
}