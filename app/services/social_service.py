import urllib.parse
from typing import List
from app.models.complaint import Complaint
from app.models.agent_state import SocialMediaDraft

class SocialEscalationService:
    """
    Generates high-impact civic escalation drafts for X (Twitter) & Instagram.
    Allows citizens and activists to publicly amplify urgent civic hazards.
    """

    ZONE_HANDLES = {
        "West": "@AMC_WestZone",
        "South": "@AMC_SouthZone",
        "North West": "@AMC_NWZone",
        "Central": "@AMC_CentralZone",
        "East": "@AMC_EastZone"
    }

    DEPARTMENT_TAGS = {
        "Roads & Buildings": "#AhmedabadRoads",
        "Solid Waste Management": "#CleanAhmedabad #SwachhBharat",
        "Light Department": "#StreetlightSafety",
        "Storm Water Drainage": "#AhmedabadMonsoon #Waterlogging"
    }

    def draft_post(self, complaint: Complaint) -> SocialMediaDraft:
        zone_handle = self.ZONE_HANDLES.get(complaint.zone, "@AhmedabadAMC")
        dept_tag = self.DEPARTMENT_TAGS.get(complaint.department, "#CivicIssue")

        post_body = (
            f"🚨 Urgent Civic Hazard Alert — {complaint.area} (Ward {complaint.ward}, {complaint.zone} Zone)!\n\n"
            f"Reported issue: {complaint.issue.value.upper()} under {complaint.department}.\n"
            f"📋 Tracking ID: {complaint.trackingId}\n"
            f"⚡ SLA Resolution Window: 24 Hours\n\n"
            f"Requesting immediate dispatch & inspection from @AhmedabadAMC {zone_handle}."
        )

        tags = [
            "#Ahmedabad",
            "#AMCAction",
            "#CivicPulseAI",
            dept_tag.split()[0]
        ]
        mentions = ["@AhmedabadAMC", zone_handle]

        full_tweet_text = f"{post_body}\n\n{' '.join(tags)}"

        # Generate 1-click web intent URL
        encoded_text = urllib.parse.quote(full_tweet_text)
        intent_url = f"https://twitter.com/intent/tweet?text={encoded_text}"

        return SocialMediaDraft(
            platform="X / Twitter",
            text=full_tweet_text,
            tags=tags,
            mentions=mentions,
            intentUrl=intent_url,
            previewHtml=f"""
            <div class="border border-slate-700/80 rounded-2xl p-4 bg-slate-900/60 backdrop-blur-md">
                <div class="flex items-center gap-2 mb-2 text-sky-400 font-semibold text-sm">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    X (Twitter) Public Escalation Draft
                </div>
                <p class="text-xs text-slate-300 whitespace-pre-line leading-relaxed">{full_tweet_text}</p>
            </div>
            """
        )
