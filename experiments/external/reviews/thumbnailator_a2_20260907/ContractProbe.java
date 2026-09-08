import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.imageio.ImageReader;
import javax.imageio.stream.ImageInputStream;
import net.coobird.thumbnailator.Thumbnails;
import net.coobird.thumbnailator.ThumbnailParameter;
import net.coobird.thumbnailator.makers.FixedSizeThumbnailMaker;
import net.coobird.thumbnailator.resizers.Resizer;
import net.coobird.thumbnailator.resizers.AbstractResizer;
import net.coobird.thumbnailator.util.exif.ExifUtils;

/** Isolated source-informed diagnostics. Never part of headline API scores. */
public class ContractProbe {
    interface Operation { void run() throws Exception; }
    static void outcome(String label, Operation operation) {
        try { operation.run(); System.out.println(label + "=completed"); }
        catch (Exception error) { System.out.println(label + "=" + error.getClass().getSimpleName() + ":" + error.getMessage()); }
    }
    public static void main(String[] args) throws Exception {
        if (args[0].equals("assertions")) {
            System.out.println("assertions_enabled=" + ContractProbe.class.desiredAssertionStatus());
            assert false : "sentinel assertion must fail when enabled";
            System.out.println("sentinel_survived=true");
            return;
        }
        System.out.println("ORIGINAL_FORMAT_is_null=" + (ThumbnailParameter.ORIGINAL_FORMAT == null));
        for (String name : new String[] {"original.jpg", "orientation_6.jpg"}) {
            ImageReader reader = ImageIO.getImageReadersByFormatName("jpg").next();
            try (ImageInputStream input = ImageIO.createImageInputStream(new File(args[1], name))) {
                reader.setInput(input);
                System.out.println(name + "_orientation=" + ExifUtils.getExifOrientation(reader, 0));
            } finally { reader.dispose(); }
        }
        BufferedImage image = new BufferedImage(32, 24, BufferedImage.TYPE_INT_RGB);
        outcome("two_arg_maker_defaultResizer", () -> new FixedSizeThumbnailMaker(50, 50).defaultResizer().make(image));
        outcome("two_arg_maker_defaultResizerFactory", () -> new FixedSizeThumbnailMaker(50, 50).defaultResizerFactory().make(image));
        outcome("fully_configured_maker", () -> {
            BufferedImage result = new FixedSizeThumbnailMaker(50, 50, true, true).make(image);
            if (result.getWidth() != 50 || result.getHeight() != 38) throw new Exception("Unexpected dimensions: " + result.getWidth() + "x" + result.getHeight());
        });
        outcome("unsupported_output_format", () -> Thumbnails.of(image).size(10, 10).outputFormat("superfakeformat"));
        outcome("three_byte_exif", () -> ExifUtils.getOrientationFromExif(new byte[] {0, 1, 2}));
        outcome("interface_getRenderingHints", () -> Resizer.class.getMethod("getRenderingHints"));
        outcome("abstract_resizer_getRenderingHints", () -> AbstractResizer.class.getMethod("getRenderingHints"));
        outcome("null_constant_equals", () -> ThumbnailParameter.ORIGINAL_FORMAT.equals(null));
    }
}
