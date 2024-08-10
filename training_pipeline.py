import kfp
from kfp import dsl
import yaml


def build_volume():
    vop = dsl.VolumeOp(
        name="Create PVC",
        resource_name="training-pipeline-pvc",
        size="1Gi",
        modes=dsl.VOLUME_MODE_RWO
    )
    return vop


def read_data_op():
    return dsl.ContainerOp(
        name="Read Data",
        image="julionevadod/clickbait-detector-kubeflow:dev",
        command=["sh", "-c"],
        arguments=["cd kedro/clickbait-detector-kedro && kedro run -p data_loading --params input_data_location=https://ml-coding-test.s3.eu-west-1.amazonaws.com/webis_train.csv,intermediate_path=/mnt/data/"],
        pvolumes={"/mnt": build_volume().volume}
    )


def cleanse_data_op():
    return dsl.ContainerOp(
        name="Cleanse Data",
        image="julionevadod/clickbait-detector-kubeflow:dev",
        command=["sh", "-c"],
        arguments=[
            "cd kedro/clickbait-detector-kedro && kedro run -p data_cleansing --params intermediate_path=/mnt/data/"],
        pvolumes={"/mnt": read_data_op().pvolume}
    )


def train():
    # return dsl.ContainerOp(
    #     name="Train ML",
    #     image="julionevadod/clickbait-detector-kubeflow:dev",
    #     command=["sh", "-c"],
    #     arguments=[
    #         "cd ../../  && mkdir logs && mkdir data/checkpoints && torchrun --nproc-per-node=2 --nnodes=1 --node-rank=0 --rdzv-id=456 --rdzv-backend=static --rdzv-endpoint=localhost:12357  --master-addr=localhost --master-port=12359 training/train.py"],
    #     pvolumes={"/mnt": cleanse_data_op().pvolume}
    # )
    with open("training-job.yml") as stream:
        pytorchjob_spec = yaml.safe_load(stream)
    return dsl.ResourceOp(
        name="Train Clickbait Detector",
        k8s_resource=pytorchjob_spec,
        action='apply',
        # success_condition='status.conditions.#(type=="Succeeded")#|#(status=="True")#',
        # failure_condition='status.conditions.#(type=="Failed")#|#(status=="True")#',
    )


@dsl.pipeline(
    name="Clickbait Detection Training Pipeline",
    description="A pipeline that performs full E2E ML workflow, from data ingestion to model training"
)
def simple_pipeline():
    return train().after(cleanse_data_op())


if __name__ == "__main__":
    pipeline_conf = dsl.PipelineConf()
    pipeline_conf.set_image_pull_policy("Always")
    kfp.compiler.Compiler().compile(
        simple_pipeline,
        "training_pipeline.yaml",
        pipeline_conf=pipeline_conf
    )
