import React, { Component } from 'react';
import GoogleMapReact from 'google-map-react';

const AnyReactComponent = ({ text }) => <div>{text}</div>;

class Map extends Component {
  static defaultProps = {
    center: {
      lat: -25.969961,
      lng: 133.704294
    },
    zoom: 4
  };

  render() {
    return (
      // Important! Always set the container height explicitly
      <div style={{ height: '70vh', width: '100%' }}>
        <GoogleMapReact
          bootstrapURLKeys={{ key: "AIzaSyAw0v3dDQwm7I4ex-_lI-kjwAKu8tEb3aU" }}
          defaultCenter={this.props.center}
          defaultZoom={this.props.zoom}
        >
          <AnyReactComponent
            lat={-25.969961}
            lng={133.704294}
            text={'Australia'}
          />
        </GoogleMapReact>
      </div>
    );
  }
}

export default Map;
