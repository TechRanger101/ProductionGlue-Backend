from prompts import *
from utils import *
from tools import *
from map import *


class Assistant():
    def __init__(self, userId) -> None:
        self.id = userId

        self.initialize()

    def initialize(self) -> None:
        self.start_prompt = get_start_prompt()
        self.system_prompt = get_system_prompt()
        self.func_prompt = get_func_call_prompt()
        self.knowledge_prompt = get_knowledge_prompt()

        self.history = [self.start_prompt]

        self.tools_dict = {
            "search_from_location_and_radius": search_place_in_radius,
            "retrieve_detailed_information_by_venue_name": search_knowledge_assistant,
            "search_venues_with_specific_attributes_by_user_query": search_knowledge_assistant,
            "retrieve_detailed_information_by_vendor_name": search_knowledge_assistant,
            "search_vendors_with_specific_attributes_by_user_query": search_knowledge_assistant
        }

        self.data = place_data.copy()

    def aisearch(self, query):
        messages = [{"role": "user", "content": query}]
        function_response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0,
            tools=tools,
            tool_choice='auto',
            stream=True
        )

        is_tool_call = False
        search_query = ""
        for chunk in function_response:
            func_message = chunk.choices[0].delta
            content = func_message.content
            if content is None and func_message.tool_calls is not None:
                is_tool_call = True
                search_query += func_message.tool_calls[0].function.arguments
            elif content is not None and not is_tool_call:
                search_query = query
                break
        
        print(search_query)

        return search_knowledge(search_query, 15)

    def chat(self, user_query):
        self.history.append({"role": "user", "content": user_query})
        if len(self.history) <= 5:
            messages = [self.system_prompt] + self.history
            # messages = [self.system_prompt, {"role": "user", "content": user_query}]
        else:
            messages = [self.system_prompt] + self.history[-5:]

        function_response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0,
            tools=tools,
            tool_choice='auto',
            stream=True
        )

        output = ""
        is_tool_call = False
        func_args = ""
        for chunk in function_response:
            func_message = chunk.choices[0].delta
            content = func_message.content
            if content is None and func_message.tool_calls is not None:
                if not is_tool_call: 
                    tool_calls = func_message.tool_calls
                    message = func_message
                is_tool_call = True
                func_args += func_message.tool_calls[0].function.arguments
            elif content is not None and not is_tool_call:
                output += content
                yield f"data: {json.dumps({'token': content})}\n\n".encode("utf-8")

        print(func_args)

        if is_tool_call:
            messages.append(message)
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_to_call = self.tools_dict[func_name]
                func_args = json.loads(func_args)
                if func_name == "search_from_location_and_radius":
                    if func_args.get('search_type') is None:
                        func_args['search_type'] = 'venue'
                        data = self.data['venue'] + self.data['vendor']
                        radius = 5 if func_args['radius'] > 5 else func_args['radius']
                        search_result = func_to_call(func_args['location'], radius, data)
                    else:
                        radius = 5 if func_args['radius'] > 5 else func_args['radius']
                        search_result = func_to_call(func_args['location'], radius, self.data[func_args.get('search_type')])
                    
                    func_response = convert_Decimal_to_float(search_result)
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": func_response
                        }
                    )
                    messages.append(self.knowledge_prompt)
                elif func_name == "retrieve_detailed_information_by_venue_name":
                    venue_name = func_args['venue']
                    query = f"venue: {venue_name}, \n{func_args.get('extra_query', '')}, type: venue" 
                    func_response = func_to_call(query)
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": func_response
                        }
                    )
                elif func_name == "search_venues_with_specific_attributes_by_user_query":
                    func_args['type'] = 'venue'
                    queries = json.dumps(func_args)
                    func_response = func_to_call(queries, 20)
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": func_response
                        }
                    )
                    messages.append(self.knowledge_prompt)
                elif func_name == "retrieve_detailed_information_by_vendor_name":
                    vendor_name = func_args['vendor']
                    queries = f"name: {vendor_name}, \n{func_args.get('extra_query', '')}, type: vendor" 
                    func_response = func_to_call(queries, 20)
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": func_response
                        }
                    )
                elif func_name == "search_vendors_with_specific_attributes_by_user_query":
                    func_args['type'] = 'vendor'
                    queries = json.dumps(func_args)
                    func_response = func_to_call(queries, 20)
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": func_response
                        }
                    )
                    messages.append(self.knowledge_prompt)

            response = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=messages,
                temperature=0.7,
                stream=True,
                max_tokens=4000
            )
            
            output = ""
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content is not None:
                    output += content
                    yield f"data: {json.dumps({'token': content})}\n\n".encode("utf-8")

        self.history.append({'role': 'assistant', 'content': output})