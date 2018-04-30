import React, { Component } from 'react'
import GoogleMapReact from 'google-map-react'


const AnyReactComponent = ({ text }) => <div>{ text }</div>;
export default class Map extends Component {
  static defaultProps = {
    center: { lat: -24.0, lng: 130.0 },
    zoom: 11
  }
render() {
    return (
      <div className='google-map'>
        <GoogleMapReact
          defaultCenter={ this.props.center }
          defaultZoom={ this.props.zoom }>
          <AnyReactComponent
            lat={ -24.0 }
            lng={ 130.0 }
          />
        </GoogleMapReact>
      </div>
    )
  }
}
