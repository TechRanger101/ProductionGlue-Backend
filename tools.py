tools = [
    {
        "type": "function",
        "function": {
            "name": "search_venues_with_specific_attributes_by_user_query",
            "description": "Utilizing NLP, the enhanced_search_venues function simplifies venue finding by interpreting conversational queries. It can process a variety of search criteria—type, capacity, and location—to deliver precise venue matches, accommodating both broad and specific user needs efficiently.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Address of the venue, the addressline, city, state and country. e.g. address: 4178 Koval Lane, city: Las Vegas, state: NV, country: United States"
                    },
                    "venueName": {
                        "type": "string",
                        "description": "The venue name. e.g. Empire Hotel"
                    },
                    "spaceName": {
                        "type": "string",
                        "description": "The space name of the venue"
                    },
                    "serviceType": {
                        "type": "string",
                        "enum": ["Apartment", "Arena", "Art Gallery", "Atrium", "Auditorium", "Ballroom", "Bar", "Basketball Court", "Black Box", "Boardroom", "Bowling Alley", "Cabaret", "Café", "Car Park", "Chapel", "Church", "Classroom", "Clubhouse", "Colosseum", "Conference Room", "Courtyard", "Covered Outdoor Space", "Cruise", "Dance Studio", "Dining Hall", "Dining Room", "Drill Hall", "Event Space", "Exhibit Hall", "Exterior of Building", "Fieldhouse", "Foyer", "Gallery", "Garden", "Greenroom", "Gym", "Hall", "Hangar", "Hotel", "Ice Rink", "Island", "Kitchen", "Library", "Lobby", "Locker Room", "Loft", "Lounge", "Meeting Room", "Museum", "Music Hall", "National Park", "Nightclub", "Office", "Outdoor", "Park (Private)", "Park (Public)", "Patio", "Pavilion", "Penthouse", "Performance Hall", "Pier", "Plaza", "Pool Deck", "Pop Up Space", "Pre-Function", "Public Plaza", "Raw", "Reception Hall", "Reception Room", "Red Carpet Area", "Restaurant", "Retail Space", "Rooftop", "Rotunda", "Salon", "Screening Room", "Shopping Center", "Skybox", "Soundstage", "Sports Complex", "Stadium", "Stage", "Station", "Studio", "Suite", "Sundeck", "Tea Room", "Terrace", "Theater", "TV Studio", "Warehouse", "White Box", "Winery", "Work Area"],
                        "description": "The type of venue space."
                    },
                    "standingCapacity": {
                        "type": "number",
                        "description": "The standing capacity of the venue. e.g. 150"
                    },
                    "seatedCapacity": {
                        "type": "number",
                        "description": "The seated capacity of the venue. e.g. 100"
                    },
                    "squareFeet": {
                        "type": "number",
                        "description": "The square feet of the venue. e.g. 2000"
                    },
                    "spaceSizeCapacity": {
                        "type": "string",
                        "enum": ["Very Small", "Small", "Medium", "Large", "Very Large"],
                        "description": "The space size capacity"
                    },
                    "spaceSizeSquareFeet": {
                        "type": "string",
                        "enum": ["Very Small", "Small", "Medium", "Large", "Very Large"],
                        "description": "The space size square feet"
                    },
                    "pgVenueBoxLink": {
                        "type": "string",
                        "description": "The website link of venue box. e.g. https://bedrock.box.com/s/lfcjten81bhxj3z9z9u81q00nyqg5arx"
                    },
                    "websiteUrl": {
                        "type": "string",
                        "description": "The website link of the venue. e.g. https://hermesworldwide.com/"
                    },
                    "phoneNumber": {
                        "type": "string",
                        "description": "Phone number of the venue. e.g. (786) 975-2550"
                    },
                    "zipcode": {
                        "type": "string",
                        "description": "Zip code of the venue. e.g. zipcode: 33139"
                    },
                    "extra_query": {
                        "type": "string",
                        "description": "Extra query related to venue in dictionary format like content about event. e.g. wedding, music festival, etc"
                    }
                },
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_vendors_with_specific_attributes_by_user_query",
            "description": "Utilizing NLP, the enhanced_search_vendors function simplifies vendor finding by interpreting conversational queries. It can process a variety of search service-Category, active cities, and location—to deliver precise vendor matches, accommodating both broad and specific user needs efficiently.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Address of the vendor, the addressline, city, state and country. e.g. address: 4178 Koval Lane, city: Las Vegas, state: NV, country: United States"
                    },
                    "vendorName": {
                        "type": "string",
                        "description": "The vendor name. e.g. Hermes Worldwide, Inc."
                    },
                    "serviceCategory": {
                        "type": "string",
                        "enum": ["Apparel & Swag", "Audio, Video, Lighting", "Business, Marketing, Finance & Legal", "Catering & Hospitality", "Entertainment & Attractions", "Event Production", "Health, Safety & Security", "Logistics & Operations", "Miscellaneous", "Permitting & Engineering", "Personnel & Talent", "Scenic & Staging", "Tenting & Event Services", "Trade-Based Labor", "Trucking & Transportation", "Venue Services"],
                        "description": "The category of the vendor service."
                    },
                    "fullServiceOffered": {
                        "type": "string",
                        "description": "full services of the vendor that encompass the complete range of their offered products or solutions. It can be several ones among 3D Pinting, 3D Scanning, 3D Sculpting & Fabrication, 3D Visualization, A/V, Acrylics, Activities, Amusement Parks, Animantronics, Arcade, Architect, Art handling, Art Installations, Artist, Attorney, Audio, Automation & Show Control, Awnings, Backline, Barricade, Bicycles, BOH Catering, BOH Furniture, BOH Supplies, Brand Ambassadors, Broadcast, Building Conservation, Car Rentals, Carpet, Catering, Chauffeur, Cleaning Company, Client, Clothing Blanks, CNC Machine, Competitor Agency, Comupters, Construction, Consulting, Content, Costume Rental, Costumes, Court, COurtside Seating, COVID testing, CPA, Craft Services, Credentials, Crowd Control, Custom App Creation, Custom Fabrication, Custom Flag, Custom Stair Manufacturing, Customization, Customization Equipment, Data Capture, Decor, Design Agency, Disc Jockey, Disinfection, Display, Document Shredding, Drape, Dumpsters, Electric, EMS, EMT, Event Consulting & Management, Expendables, Experiental Agency, Fencing, Finishing, FII, Flooring, Floral, Florist, FOH Catering, Food & Beverage, Fuel, Furniture, Games, General Contractor, Giveaways, Glass, glue HR, Golf Carts, Graphic Design, Graphics, Greenroom Trailer, Hardware, Heavy Equipment, Hotel, HVAC, Independent Contractor-Staffing, Inflatables, Injection Molding, Installation, Instrument Repair, Insurance, Interactive, Internet, Interpreters, IT, Kites, Labor, Landscaping, Laser Cutting, Legal Consultation, Licensed Electrician, Lighting, Livestreaming, Lockers, Logistics Management, Lumber, Makeup Artist, Mannequins, Marketing, Mascots, Metal Fabricator, Model Makers, Motion Design, Movie Studio, Museum Exhibits, Music Composition, Music Licensing, N/A, Neon, Non Profit Organization, Non-Union, NYPD, Office Trailer, Online Ordering-No Rep, Packaging, Paint Shop, Parking, Party Planning, Patches/Pins, Payroll, Pedestals, Permitting &/or Engineering, PG Account-See Notes, PG Internal, Photo Booth, Photography, Piano, Pipe and Drape, Plastics, Playgrounds, PortAJohns, Power, Previsualization, Private Chef, Prizes, Production Management, Production Supplies, Programming, Promotional Products, Propane, Props, Prototyping, Radios, Real Estate, Recruitment Agency, Refinishing, Rendering Artist, Rental Furniture, Rentals, Restoration, Restroom Trailer, Retail Displays, Rides, Rigging, Scene Shop, Scenic, Scenic Design, Security, SEG, Signage, Signs & Advertising, Site, Soft Goods, Sound, Special Effects, Sports Equipment, Staffing, Staging, Stair Fabrication, Stanchions, Storage, Storefront, T Shirt Printing, Talent, Teleprompter, Temporary Walls, Tension Fabric Structures, Tenting, Theme Parks, Tools, Trade Show, Traffic Control, Trnasportation, Trucking, union, Upholstery, Vehicle Wraps, Venue, Video, Video Production Trailers, VinyI, Virtual Event Platform, Virtual Misc, Warehousing, Waste Management, Water Weather, Webcast, Welding Curtain, Work Out-gluePEEPS, Composting, Translation, Translation, Closed Captioning, Transcription, Flying, Travel Management, Recording, Wall Covering, ADA Lift, ASL Services, Swag, Coffee Cart, Cameras, Camera Operator"
                    },
                    "status": {
                        "type": "string",
                        "description": "The status of the vendor. It can be one of Active Vendor, Research/No PG Contact, Potential Vendor or Inactive."
                    },
                    "YearOfNda": {
                        "type": "string",
                        "desription": "The year of NDA contract e.g. 2024"
                    },
                    "activeCities": {
                        "type": "string",
                        "description": "The active cities of vendor where the vendor's sevices are available. It can be several addresses separated by ';'. e.g. New York, NY, United States, 100; Jersey City, NJ, United States, 030; Denver, CO, United States, 80022"
                    },
                    "websiteUrl": {
                        "type": "string",
                        "description": "The website link of the vendor. e.g. https://hermesworldwide.com/"
                    },
                    "email": {
                        "type": "string",
                        "description": "The contact email of the vendor. e.g. info@breesstudio.com"
                    },
                    "phoneNumber": {
                        "type": "string",
                        "description": "Phone number of the vendor. e.g. (786) 975-2550"
                    },
                    "zipcode": {
                        "type": "string",
                        "description": "Zip code of the vendor. e.g. zipcode: 33139"
                    },
                    "extra_query": {
                        "type": "string",
                        "description": "Extra query related to vendor in dictionary format like content about event. e.g. wedding, music festival, etc"
                    }
                },
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_detailed_information_by_venue_name",
            "description": "Detect venue name and space name, and retrieve detailed information by detected venue name",
            "parameters": {
                "type": "object",
                "properties": {
                    "venue": {
                        "type": "string",
                        "description": "The venue name and space name. For example, input: 'What information do you have on the Empire Hotel?' output: 'venue: Empire Hotel', input: 'I'd like to know ROW DTLA | North Lot' output: 'venue: ROW DTLA | North Lot'"
                    },
                    "extra_query": {
                        "type": "string",
                        "description": "Extra query related to venue in dictionary format like addressline, city, state and country. For example, input: 'Empire Hotel in New York' output: 'city: New York, state: NY, country: United States'"
                    }
                },
                "required": ["venue"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_detailed_information_by_vendor_name",
            "description": "Detect vendor name, and retrieve detailed information by detected vendor name",
            "parameters": {
                "type": "object",
                "properties": {
                    "vendor": {
                        "type": "string",
                        "description": "The vendor name. For example, input: 'What information do you have on the Hermes Worldwide, Inc.?' output: 'vendor: Hermes Worldwide, Inc.', input: 'I'd like to know 3D Exhibits' output: 'vendor: 3D Exhibits'"
                    },
                    "extra_query": {
                        "type": "string",
                        "description": "Extra query related to vendor in dictionary format like addressline, city, state and country. For example, input: 'Hermes Worldwide, Inc. in Denver' output: 'city: Denver, state: CO, country: United States'"
                    }
                },
                "required": ["vendor"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_from_location_and_radius",
            "description": "Detect venue/vendor, location and radius from user's query and search venues/vendors in the given radius from the given location. The radius must be given by the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The zipcode or the address, city, state and country, e.g. 10012, V5K 0B1, San Francisco, CA, United States, Hong Kong"
                    },
                    "radius": {
                        "type": "number",
                        "description": "The radius from the location. the unit must be km. This value must be given by the user."
                    },
                    "search_type": {
                        "type": "string",
                        "enum": ["venue", "vendor"],
                        "description": "The type the user is looking for."
                    }
                },
                "required": ["location", "radius"]
            }
        }
    },
]