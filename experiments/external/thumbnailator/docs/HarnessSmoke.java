import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;

import net.coobird.thumbnailator.Thumbnails;

public final class HarnessSmoke {
    public static void main(String[] args) throws Exception {
        BufferedImage source = new BufferedImage(32, 24, BufferedImage.TYPE_INT_RGB);
        source.setRGB(0, 0, Color.BLUE.getRGB());
        BufferedImage result = Thumbnails.of(source).size(16, 16).asBufferedImage();
        if (result.getWidth() != 16 || result.getHeight() != 12) {
            throw new AssertionError("unexpected dimensions");
        }
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        Thumbnails.of(source).size(8, 8).outputFormat("png").toOutputStream(out);
        if (out.size() == 0) {
            throw new AssertionError("empty PNG");
        }
        System.out.println("__DONE__ thumbnailator smoke " + out.size());
    }
}
