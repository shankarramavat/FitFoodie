# ml_model.py (replace your food_identifier function with this)

import os
from dotenv import load_dotenv
load_dotenv()
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

# keep your channel/stub initialization as you already have it
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

# Use env var for key (set CLARIFAI_API_KEY in your environment)
CLARIFAI_KEY = os.getenv("CLARIFAI_API_KEY")
metadata = (("authorization", "Key " + CLARIFAI_KEY),)

userDataObject = resources_pb2.UserAppIDSet(user_id="clarifai", app_id="main")


def food_identifier(image_data):
    """
    Given `image_data` (bytes), call Clarifai food-item-recognition model
    and return the top predicted concept name. Raises RuntimeError with diagnostic
    details on failure.
    """
    # Use bytes directly
    file_bytes = image_data

    try:
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id="food-item-recognition",
                version_id="1d5fd481e0cf4826aa72ec3ff049e044",
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(base64=file_bytes)
                        )
                    )
                ],
            ),
            metadata=metadata,
        )
    except Exception as e:
        # network / client-level error
        msg = f"Exception calling Clarifai stub.PostModelOutputs: {e}"
        print(msg)
        raise RuntimeError(msg) from e

    # DEBUG: print top-level status and raw response summary for diagnostics
    try:
        top_status = post_model_outputs_response.status
        print("Clarifai top-level status:", top_status.code, top_status.description)
    except Exception:
        print("Could not read top-level status from response:", post_model_outputs_response)

    # If the API-level status indicates failure, show details and abort
    if getattr(post_model_outputs_response, "status", None) is not None and post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        # safe printing: prefer top-level status fields
        code = post_model_outputs_response.status.code
        desc = post_model_outputs_response.status.description
        details = getattr(post_model_outputs_response.status, "details", None)
        msg = f"Clarifai API returned failure. code={code}, description={desc}, details={details}"
        print(msg)
        raise RuntimeError(msg)

    # Ensure outputs exist
    outputs = getattr(post_model_outputs_response, "outputs", None)
    if not outputs:
        # No outputs. Log full response (string) for debugging
        raw = str(post_model_outputs_response)
        msg = "Clarifai returned no outputs. Full response: " + raw
        print(msg)
        raise RuntimeError(msg)

    # get the first output (safe since we checked)
    output = outputs[0]

    # Ensure expected fields exist
    if not getattr(output, "data", None) or not getattr(output.data, "concepts", None):
        print("Output has no data.concepts. Full output:", output)
        raise RuntimeError("Model output missing concepts")

    # Print predicted concepts for debugging
    print("Predicted concepts:")
    for concept in output.data.concepts:
        print("\t%s %.2f" % (concept.name, concept.value))

    # Return top concept's name
    return output.data.concepts[0].name
