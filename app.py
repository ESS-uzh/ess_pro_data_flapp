from flask import Flask, render_template, request, jsonify
import folium
import json

app = Flask(__name__)

# Load project data from JSON file
with open("data/projects.json") as f:
    projects = json.load(f)

# Research topics and images
TOPICS = {
    "Biodiversity": [
        "biodiversity_img.jpg",
        "Biodiversity refers to the variety of life forms on Earth, encompassing different species, ecosystems, and genetic diversity.",
    ],
    "Climate Change": ["climate_change_img.png", " climate change is .."],
    "Ecosystem Services": ["ecosystem_services_img.jpg", "ecosystems services is .."],
    "Social Ecological Systems": ["sus_dev_img.png", " sustenaible development is .."],
}

# Prepare the data for the map
project_locations = [(p["lat"], p["lon"], p["name"]) for p in projects]
recent_projects = ["frog.jpg", "pappagalli.jpg", "river.jpg"]


@app.context_processor
def inject_topics():
    return dict(
        research_topics={
            "Biodiversity": "biodiversity.jpg",
            "Climate Change": "climate_change.jpg",
            "Ecosystem Services": "ecosystem_services.jpg",
            "Social-Ecological Systems": "social_ecological.jpg",
        }
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        research_topics=TOPICS,
        projects=projects,
        project_locations=project_locations,
        recent_projects=recent_projects,
        generate_map=generate_map_home_page,  # Pass the function to the template
    )


@app.route("/topic/<string:topic_name>")
def topic_page(topic_name):
    """Page for a specific research topic with project filtering."""
    topic_projects = [p for p in projects if topic_name in p["tags"]]
    project_locations = [(p["lat"], p["lon"], p["name"]) for p in topic_projects]
    topic_description = TOPICS[topic_name][1]
    return render_template(
        "topic_page.html",
        topic_name=topic_name,
        topic_description=topic_description,
        projects=topic_projects,
        project_locations=project_locations,
        generate_map=generate_map,
    )


@app.route("/project/<int:project_id>")
def project_page(project_id):
    """Detailed page for a specific project."""
    project = next((p for p in projects if p["id"] == project_id), None)
    return render_template(
        "project_page.html",
        project=project,
        generate_map=generate_map,  # Pass the function to the template
    )


# Folium Map Generator
def generate_map_home_page(locations, center=[10.245731, -28.782217], zoom_start=2):
    folium_map = folium.Map(
        location=center, zoom_start=zoom_start, tiles="Cartodb Positron"
    )

    for lat, lon, name in locations:
        if lat and lon:
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,  # Adjust dot size
                color="white",  # Border color
                fill=True,
                fill_color="blue",  # Fill color
                fill_opacity=0.7,
                popup=name,
            ).add_to(folium_map)

    return folium_map._repr_html_()


# Folium Map Generator
def generate_map(locations, center=[30.079227, -21.750656], zoom_start=2, polygon=None):
    folium_map = folium.Map(
        location=center, zoom_start=zoom_start, tiles="OpenStreetMap"
    )

    # Add markers or polygon to the map
    if polygon:
        folium.Polygon(
            locations=polygon, color="blue", fill=True, fill_opacity=0.4
        ).add_to(folium_map)
    else:
        for lat, lon, name in locations:
            if lat and lon:
                folium.Marker(
                    [lat, lon], popup=name, icon=folium.Icon(color="blue")
                ).add_to(folium_map)

    return folium_map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)
