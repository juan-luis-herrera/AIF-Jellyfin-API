# AIF-Media-API

## What is this repository?

This is a small Proof-of-Concept implementation of the Service Configuration API, as proposed in the Internet Computing paper. For now, it implements the API in the Media streaming use case.

It also includes some additional files for development, deployment, and testing.

## What do I need to run this?

At the very least, you will need a container runtime. `docker` is recommended, as it was used for testing and development, but `podman` may work too. `docker-compose` is recommended to run the container specification. You can also set up the containers manually or through other tools to follow the specification.

For proper testing, you may also want to create automated clients.

## Repository structure

- `Bruno`: API tests using the open-source [Bruno](https://www.usebruno.com/) tool.
    -  `JellyfinAPI`: Tests for the Jellyfin API,
- `jellyfin_conf`: Jellyfin configuration, provided empty for security reasons. **Create this directory if it does not exist**.
- `jelllyfin_data`: Media for Jellyfin to stream, provided empty for data size and copyright reasons. **Create this directory if it does not exist**.
    - `music`: Music files. Refer to the setup details below to replicate the experiment, or add your own.
    - `movies`: Video files. Refer to the setup details below to replicate the experiment, or add your own.
- `docker-compose-jellyfin-test.yaml`: Docker Compose specification for the scenario.
- `ServiceAPIExample.yml`: Example declaration of the Service API using the OpenAPI specification.
- `README.md`: Current file

## Setup details (for replicability)

### Tools and data used

- Tool used to generate the basis of the Service API: openapi-generator 7.14.0-1 (installed via pacman)
- Music: Royalty-free, legally obtained from [Classicals.de](https://classicals.de) in MP3 format. Specifically:
    - Bach - Air on the G String - BWV 1068 - Arranged for Woodwinds and Strings
    - Beethoven - Für Elise - Bagatelle No. 25 - WoO 59
    - Beethoven - Ode to Joy - Symphony No. 9, Op. 125 - Arranged for Piano
    - Brahms - Lullaby : Wiegenlied - Op. 49, No. 4 - Arranged for Music Box
    - Dvořák - Humoresques - Op. 101 B. 187 No. 1 - 8 (Complete) & B. 138 - Concert Grand Mix
    - Haydn - Piano Sonata in C major - 1. Movement - Hoboken XVI-7
    - Johann Strauss II - The Blue Danube - Op. 314
    - Mozart - Eine Kleine Nachtmusik - Allegro (Advent Chamber Orchestra)
    - Mozart - Requiem in D minor, K.626 - IIIa. Dies Irae - Arranged for Piano
    - Mozart - Requiem in D minor, K.626 - VII. Lacrimosa - Arranged for Harpsichord
    - Schubert - Serenade - Schwanengesang, No. 4 - D. 957 - Arranged for Music Box
    - Tchaikovsky - Swan Lake, Op. 20 - Act 2 - Part 1
    - Saint-Saens - Carnival of the Animals - 07 - Aquarium
    - Saint-Saens - Carnival of the Animals - 12 - Fossiles (Fossils)
- Movies: Public Domain movies, legally obtained from Wikipedia in WEBM format. Specifically:
    - Night of the Living Dead (1968)
    - Popeye The Sailor - Aladding and His Wonderful Lamp (1939)
    - The Emperor Jones (1933) by Dudley Murphy

### Instructions

1. Create the `jellyfin_conf` and `jellyfin_data` folders, if they do not already exist. Populate `jellyfin_data/music` and `jellyfin_data/movies` with the media you wish to use. **Make sure you have the legal right to offer this media in your jurisdiction**, even if you use the public domain or royalty-free media referenced above.
2. Start up the services: `docker-compose -f docker-compose-jellyfin-test.yaml up`.
3. Access Jellyfin (by default at `http://localhost:8096`) and complete the setup.
4. Access the Dashboard at Jellyfin and generate an API key to be used in the test.

## Disclaimer

This repository does not provide any media files, they must be provided by the user or operator. The responsibles and contributors of this project deny all responsability and accountability on the obtention and provision of media with this software. It is the user's or operator's responsability to ensure they have the right to legally offer this media in their jurisdiction. None of the statements in this repository constitutes legal advice.