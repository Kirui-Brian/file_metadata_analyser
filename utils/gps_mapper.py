"""
GPS Mapper Utility
Creates interactive maps from GPS coordinates extracted from images.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    import folium
    from folium import plugins
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False


class GPSMapper:
    """
    Creates interactive maps from GPS coordinates.
    """
    
    def __init__(self):
        """Initialize the GPS mapper."""
        self.geocoder = None
        if GEOPY_AVAILABLE:
            self.geocoder = Nominatim(user_agent="file_metadata_analyzer")
    
    def create_map(self, gps_data: Dict[str, Any], output_path: str) -> bool:
        """
        Create an interactive map from GPS coordinates.
        
        Args:
            gps_data (Dict): GPS data containing coordinates
            output_path (str): Path to save the HTML map
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not FOLIUM_AVAILABLE:
            print("Error: folium library not available. Install with: pip install folium")
            return False
        
        lat = gps_data.get('latitude_decimal')
        lon = gps_data.get('longitude_decimal')
        
        if lat is None or lon is None:
            print("Error: No valid GPS coordinates found")
            return False
        
        # Create map centered on coordinates
        m = folium.Map(
            location=[lat, lon],
            zoom_start=15,
            tiles='OpenStreetMap'
        )
        
        # Get location name if possible
        location_name = self._get_location_name(lat, lon)
        
        # Create popup text
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <b>GPS Coordinates</b><br>
            Latitude: {lat}<br>
            Longitude: {lon}<br>
        """
        
        if 'altitude_meters' in gps_data:
            popup_html += f"Altitude: {gps_data['altitude_meters']} meters<br>"
        
        if location_name:
            popup_html += f"<br><b>Location:</b><br>{location_name}"
        
        popup_html += "</div>"
        
        # Add marker
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip="Photo Location",
            icon=folium.Icon(color='red', icon='camera', prefix='fa')
        ).add_to(m)
        
        # Add circle to show approximate area
        folium.Circle(
            [lat, lon],
            radius=100,
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.2,
            popup='Approximate location area'
        ).add_to(m)
        
        # Add coordinate display
        plugins.MousePosition().add_to(m)
        
        # Save map
        m.save(output_path)
        return True
    
    def create_multi_location_map(self, locations: List[Dict[str, Any]], output_path: str) -> bool:
        """
        Create a map with multiple locations.
        
        Args:
            locations (List[Dict]): List of GPS data dictionaries
            output_path (str): Path to save the HTML map
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not FOLIUM_AVAILABLE:
            print("Error: folium library not available")
            return False
        
        if not locations:
            print("Error: No locations provided")
            return False
        
        # Calculate center point
        lats = [loc['gps_data']['latitude_decimal'] for loc in locations 
                if 'gps_data' in loc and 'latitude_decimal' in loc['gps_data']]
        lons = [loc['gps_data']['longitude_decimal'] for loc in locations 
                if 'gps_data' in loc and 'longitude_decimal' in loc['gps_data']]
        
        if not lats or not lons:
            print("Error: No valid coordinates found")
            return False
        
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Add markers for each location
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']
        
        for i, loc in enumerate(locations):
            gps_data = loc.get('gps_data', {})
            lat = gps_data.get('latitude_decimal')
            lon = gps_data.get('longitude_decimal')
            
            if lat is None or lon is None:
                continue
            
            filename = loc.get('file_info', {}).get('filename', f'Location {i+1}')
            color = colors[i % len(colors)]
            
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px;">
                <b>File:</b> {filename}<br>
                <b>Coordinates:</b><br>
                Latitude: {lat}<br>
                Longitude: {lon}<br>
            </div>
            """
            
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=filename,
                icon=folium.Icon(color=color, icon='camera', prefix='fa')
            ).add_to(m)
        
        # Add lines connecting locations in sequence
        if len(lats) > 1:
            folium.PolyLine(
                locations=list(zip(lats, lons)),
                color='blue',
                weight=2,
                opacity=0.5
            ).add_to(m)
        
        # Save map
        m.save(output_path)
        return True
    
    def _get_location_name(self, lat: float, lon: float) -> Optional[str]:
        """
        Get location name from coordinates using reverse geocoding.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            str: Location name or None
        """
        if not self.geocoder:
            return None
        
        try:
            location = self.geocoder.reverse(f"{lat}, {lon}", timeout=5)
            if location:
                return location.address
        except (GeocoderTimedOut, GeocoderServiceError):
            pass
        
        return None
    
    @staticmethod
    def export_coordinates_to_kml(gps_data: Dict[str, Any], output_path: str, name: str = "Location") -> bool:
        """
        Export GPS coordinates to KML format (Google Earth).
        
        Args:
            gps_data (Dict): GPS data containing coordinates
            output_path (str): Path to save the KML file
            name (str): Name for the placemark
            
        Returns:
            bool: True if successful, False otherwise
        """
        lat = gps_data.get('latitude_decimal')
        lon = gps_data.get('longitude_decimal')
        alt = gps_data.get('altitude_meters', 0)
        
        if lat is None or lon is None:
            return False
        
        kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>File Metadata GPS Data</name>
    <Placemark>
      <name>{name}</name>
      <description>GPS coordinates extracted from file metadata</description>
      <Point>
        <coordinates>{lon},{lat},{alt}</coordinates>
      </Point>
    </Placemark>
  </Document>
</kml>"""
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(kml_content)
            return True
        except Exception:
            return False
