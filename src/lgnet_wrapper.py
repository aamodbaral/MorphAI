import torch
import torch.nn as nn
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "external", "lgnet"))
from models import networks


def build_lgnet_stage1(input_nc=4, output_nc=3, ngf=64, netG="unet_256", norm="batch"):
    """Builds netG1 exactly as Pix2PixGLGModel does, at the original 4-channel input."""
    return networks.define_G(input_nc, output_nc, ngf, netG, norm,
                              use_dropout=True, init_type="normal",
                              init_gain=0.02, gpu_ids=[])


def load_pretrained_stage1(weights_path):
    net = build_lgnet_stage1(input_nc=4)  # matches checkpoint's original shape
    state_dict = torch.load(weights_path, map_location="cpu")
    # some checkpoints save under a "netG1" key, others save the raw state_dict directly
    if "netG1" in state_dict:
        state_dict = state_dict["netG1"]
    net.load_state_dict(state_dict, strict=True)
    return net


def expand_first_conv(old_conv, extra_channels=1):
    new_conv = nn.Conv2d(
        in_channels=old_conv.in_channels + extra_channels,
        out_channels=old_conv.out_channels,
        kernel_size=old_conv.kernel_size,
        stride=old_conv.stride,
        padding=old_conv.padding,
        bias=(old_conv.bias is not None),
    )
    with torch.no_grad():
        new_conv.weight[:, :old_conv.in_channels] = old_conv.weight
        new_conv.weight[:, old_conv.in_channels:] = 0.0  # new channel starts at zero contribution
        if old_conv.bias is not None:
            new_conv.bias[:] = old_conv.bias
    return new_conv


class LGNetStage1Conditioned(nn.Module):
    """
    Wraps LGNet's stage-1 UnetGenerator (netG1) to accept an extra conditioning
    channel (landmark/symmetry heatmap) on top of the original [masked_rgb(3) + mask(1)].
    """
    def __init__(self, weights_path):
        super().__init__()
        self.net = load_pretrained_stage1(weights_path)

        old_conv = self.net.model.model[0]        # confirmed path: Conv2d(4, 64, ...)
        new_conv = expand_first_conv(old_conv, extra_channels=1)
        self.net.model.model[0] = new_conv          # now Conv2d(5, 64, ...)

    def forward(self, masked_rgb, mask, heatmap):
        x = torch.cat([masked_rgb, mask, heatmap], dim=1)  # (B, 5, H, W)
        return self.net(x)