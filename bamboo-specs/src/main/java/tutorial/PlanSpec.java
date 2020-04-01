package tutorial;

import com.atlassian.bamboo.specs.api.BambooSpec;
import com.atlassian.bamboo.specs.api.builders.permission.PermissionType;
import com.atlassian.bamboo.specs.api.builders.permission.Permissions;
import com.atlassian.bamboo.specs.api.builders.permission.PlanPermissions;
import com.atlassian.bamboo.specs.api.builders.plan.Job;
import com.atlassian.bamboo.specs.api.builders.plan.Plan;
import com.atlassian.bamboo.specs.api.builders.plan.PlanIdentifier;
import com.atlassian.bamboo.specs.api.builders.plan.Stage;
import com.atlassian.bamboo.specs.api.builders.project.Project;
import com.atlassian.bamboo.specs.builders.repository.git.GitRepository;
import com.atlassian.bamboo.specs.builders.task.CheckoutItem;
import com.atlassian.bamboo.specs.builders.task.MavenTask;
import com.atlassian.bamboo.specs.builders.task.ScriptTask;
import com.atlassian.bamboo.specs.builders.task.VcsCheckoutTask;
import com.atlassian.bamboo.specs.builders.trigger.ScheduledTrigger;
import com.atlassian.bamboo.specs.util.BambooServer;

import java.util.concurrent.TimeUnit;

/**
 * Plan configuration for Bamboo.
 *
 * @see <a href="https://confluence.atlassian.com/display/BAMBOO/Bamboo+Specs">Bamboo Specs</a>
 */
@BambooSpec
public class PlanSpec {

    /**
     * Run 'main' to publish your plan.
     */
    public static void main(String[] args) {
        // by default credentials are read from the '.credentials' file
        BambooServer bambooServer = new BambooServer("http://localhost:8085");

        Plan plan = new PlanSpec().createPlan();
        bambooServer.publish(plan);

        PlanPermissions planPermission = new PlanSpec().createPlanPermission(plan.getIdentifier());
        bambooServer.publish(planPermission);
    }

    private PlanPermissions createPlanPermission(PlanIdentifier planIdentifier) {
        Permissions permissions = new Permissions()
                .userPermissions("bamboo", PermissionType.ADMIN)
                .groupPermissions("bamboo-admin", PermissionType.ADMIN)
                .loggedInUserPermissions(PermissionType.BUILD)
                .anonymousUserPermissionView();

        return new PlanPermissions(planIdentifier)
                .permissions(permissions);
    }

    private Project project() {
        return new Project()
                .name("My Project")
                .key("PROJ");
    }

    Plan createPlan() {
        return new Plan(project(), "My Plan", "PLAN")
                .description("Plan created from Bamboo Java Specs")
                .stages(
                        new Stage("Build Stage").jobs(
                                new Job("Build Job", "CJ").tasks(
                                        checkoutTask(),
                                        mavenTask()
                                )
                        ),
                        new Stage("Echo").jobs(
                                new Job("Echo1", "E1").tasks(
                                        new ScriptTask().inlineBody("echo hello Echo1"),
                                        new ScriptTask().inlineBody("echo bye Echo1")
                                ),
                                new Job("Echo2", "E2").tasks(
                                        new ScriptTask().inlineBody("echo hello Echo2"),
                                        new ScriptTask().inlineBody("echo bye Echo2")
                                )
                        )

                )
                .planRepositories(getDefaultRepo())
                .triggers(new ScheduledTrigger().scheduleEvery(30, TimeUnit.MINUTES));
//                .triggers(new RepositoryPollingTrigger().pollEvery(5, TimeUnit.MINUTES));
    }

    private GitRepository getDefaultRepo() {
        return new GitRepository()
                .name("my-repo")
                .url("https://github.com/pvkr/algs.git")
                .branch("master");
    }

    private VcsCheckoutTask checkoutTask() {
        CheckoutItem defaultRepository = new CheckoutItem().defaultRepository();
        return new VcsCheckoutTask()
                .description("Checkout")
                .cleanCheckout(false)
                .checkoutItems(defaultRepository);
    }

    private MavenTask mavenTask() {
        return new MavenTask()
                .description("Build")
                .goal("clean install")
                .hasTests(false)
                .version3()
                .jdk("JDK 1.8.0_242")
                .executableLabel("Maven 3.3");
    }
}
