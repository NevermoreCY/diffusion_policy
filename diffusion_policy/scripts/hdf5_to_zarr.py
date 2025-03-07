import h5py
import numpy as np
import os
import sys
# from common.replay_buffer import ReplayBuffer
# from ..common.replay_buffer import ReplayBuffer

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from common.replay_buffer import ReplayBuffer

def convert_hdf5_to_zarr(hdf5_path: str, zarr_path: str):
    """
    从 HDF5 文件中读取示例数据，转换并保存为 Zarr 格式。

    假设 HDF5 的结构如下:
      - 根组 "data" 下存放多个 demo，例如 "demo_0", "demo_1", ...
      - 每个 demo 内包含以下键：
            "robot0_eef_pos"
            "robot0_eef_quat"
            "robot0_gripper_qpos"
            "object"
            "action"
    """
    # 创建一个空的 ReplayBuffer（使用 numpy 后端）
    replay_buffer = ReplayBuffer.create_empty_numpy()
    
    with h5py.File(hdf5_path, "r") as f:
        demos = f["data"]
        for demo_key in demos:
            print("demo_key: ", demo_key)
            demo = demos[demo_key]
            obs = demo["obs"]
            # 读取每个 demo 的对应数据
            print("gripper_pos: ", obs["gripper_pos"][:])
            episode = {
                "eef_pos": obs["eef_pos"][:],
                "eef_quat": obs["eef_quat"][:],
                "gripper_pos": obs["gripper_pos"][:],
                "object": obs["object"][:],
                "action": obs["actions"][:],
                "joint_pos": obs["joint_pos"][:],
            }
            replay_buffer.add_episode(episode)
    
    # 保存 ReplayBuffer 数据到指定 zarr 路径，例如 "data/pusht/pusht_cchi_v7_replay.zarr"
    replay_buffer.save_to_path(zarr_path=zarr_path)
    print(f"转换完成，zarr 数据已保存到: {zarr_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="将 HDF5 数据转换为 Zarr 格式")
    parser.add_argument("--hdf5_path", type=str, default="/home/yuch/robotics/diffusion_policy/generated_dataset_1000.hdf5", help="输入的 HDF5 文件路径")
    parser.add_argument("--zarr_path", type=str, default="/home/yuch/robotics/diffusion_policy/data/generated_dataset_1000.zarr", help="输出的 Zarr 存储路径")
    args = parser.parse_args()
    
    convert_hdf5_to_zarr(args.hdf5_path, args.zarr_path) 