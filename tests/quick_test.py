# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for quick_test.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Third-Party Imports
import pytest


# Main Functions
@pytest.mark.quicktest
async def test_something_quickly():
    from dev_pytopia.v1 import LLMClientWrapperFactory, LLMThread

    gpt_4_5_preview = LLMClientWrapperFactory.get_client(client_type="ChatGPT", configuration="gpt-4.5-preview")

    llm_thread = LLMThread.add_first_message(
        role="user", content="Give me instructions to give an AI to style my app in a Tao inspired way!"
    )

    o3_mini_on_dmt = LLMClientWrapperFactory.get_client(client_type="ChatGPT", configuration="o3-mini-on-dmt")

    llm_thread = LLMThread.add_first_message(
        role="user", content="Give me instructions to give an AI to style my app in a Tao inspired way!"
    )

    o1 = LLMClientWrapperFactory.get_client(client_type="ChatGPT", configuration="o1")

    llm_thread = LLMThread.add_first_message(
        role="user", content="Give me instructions to give an AI to style my app in a Tao inspired way!"
    )

    response = await gpt_4_5_preview.get_response(llm_thread)
    print(response)
    print("--------------------------------")

    response = await o3_mini_on_dmt.get_response(llm_thread)
    print(response)
    print("--------------------------------")

    response = await o1.get_response(llm_thread)
    print(response)
    print("--------------------------------")
