from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import paddle.v2 as paddle
import progressbar
import time
from data_utils.data import DataGenerator
from model_utils.model import DeepSpeech2Model

def SpeechRecognizer():
    """Evaluate on whole test data for DeepSpeech2."""
    paddle.init(use_gpu=True,
                rnn_use_batch=True,
                trainer_count=1)
    data_generator = DataGenerator(
        vocab_filepath='models/aishell/vocab.txt',
        mean_std_filepath='models/aishell/mean_std.npz',
        augmentation_config='{}',
        specgram_type='linear',
        num_threads=8,
        keep_transcription_text=True)
    batch_reader = data_generator.batch_reader_creator(
        manifest_path='data/cctv/manifest',
        batch_size=128,
        min_batch_size=1,
        sortagrad=False,
        shuffle_method=None)

    ds2_model = DeepSpeech2Model(
        vocab_size=data_generator.vocab_size,
        num_conv_layers=2,
        num_rnn_layers=3,
        rnn_layer_size=1024,
        use_gru=True,
        pretrained_model_path='models/aishell/params.tar.gz',
        share_rnn_weights=False)

    # decoders only accept string encoded in utf-8
    vocab_list = [chars.encode("utf-8") for chars in data_generator.vocab_list]

    #if args.decoding_method == "ctc_beam_search":
    ds2_model.init_ext_scorer(2.6, 5.0, 'models/lm/zh_giga.no_cna_cmn.prune01244.klm',
                                vocab_list)
    ds2_model.logger.info("start evaluation ...")
    transcript = []
    bar = progressbar.ProgressBar(widgets=[
        progressbar.Percentage(),
        progressbar.Bar(),
        ' (', progressbar.SimpleProgress(), ') ',
        ' (', progressbar.ETA(), ') ', ])
    for infer_data in bar(batch_reader()):
        probs_split = ds2_model.infer_batch_probs(
            infer_data=infer_data,
            feeding_dict=data_generator.feeding)

        result_transcripts = ds2_model.decode_batch_beam_search(
            probs_split=probs_split,
            beam_alpha=2.6,
            beam_beta=5.0,
            beam_size=300,
            cutoff_prob=0.99,
            cutoff_top_n=40,
            vocab_list=vocab_list,
            num_processes=8)
        transcript += result_transcripts
        time.sleep(0.01)
    return transcript
