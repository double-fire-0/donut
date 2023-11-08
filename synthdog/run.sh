conda activate /hetu_group/wangyan/envs/env_minigpt4/
for i in {0..25}
do
    echo $i
    nohup synthtiger -o ./out_zh_num_1103/outputs_p${i}_4k/ -c 4000 -w 0 -v template.py SynthDoG config_zh_1031.yaml > ${i}.txt &
done
